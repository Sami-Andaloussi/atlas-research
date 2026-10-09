"""Claim 1 (card C04): do breaks follow an act that takes a support away? Each break's dated line, the described shares,
the base rate and the forward table. Told, never counted: no margin, no verdict.

M0 v4.2 section 6, claim 1, as the card writes it (readings R1-R5 are the card's). From the study's folder::

    ../../toolkit/bin/ftpy code/claim1.py

The card's readings, in short: R1 a break's entry route and tercile are those of the money's last counted frame c spell
entered at or before the onset; R2 the line's acts run from three years before the onset's year to the crossing; R3 the
shares' classes are mutually exclusive, in the order after / same year / before / no act / cannot be read (L = 3), "no act"
needing every act source to cover y-3..y+3; R4 a trial whose next three years pass the panel's common end or the spell's
end is censored; R5 a spell's supports are read at its entry.

Readings made in code, in the open (the card's own are R1-R5):

J1. *Acts*: ft001-acts lines with ``headline`` yes and ``status`` counted; the act code is the ``route`` column (T2, L1,
    L2, L3, H1), the date ``entry_date`` (the year is read, the order inside a year never), the source ``source``. Several
    lines of one act in one year (T2's creditor classes) are each printed on the line, and count once in any share.
J2. *Coverage*: an act code is covered in a year if the union of its coverage.csv rows (``T2 domestic`` and ``T2 external``
    are T2) holds it; a money with no row for a code is covered in no year. Hammond's ``L3-target`` rows are left out
    (no act was found there; the headline L3 is Garriga's). "By act source" groups the acts by source (the Bank of
    Canada-Bank of England database, Reinhart-Rogoff's Varieties, their TTID dummies, Garriga's L1 and L3, the
    chronologies' L2 and H1) and reads each group's own coverage; each group's ``windows_covered`` says for how many
    breaks it covers y-3..y+3.
J3. *A break whose onset cannot be read* (frame b's ``break_onset`` empty or "cannot be read"): no onset year, so its
    class is "cannot be read" (counted apart in ``onset_unreadable``), its line lists the acts from three years before
    the crossing's year to the crossing, and R1's spell is the last one entered at or before the crossing.
J4. *The shares read acts in y-3..y+3* whether or not they fall after the crossing (the card's R3 as written); the line
    (R2) stops at the crossing.
J5. *Strained at-risk years*: the years y >= 1970 of a counted spell, entry <= y <= entry + H - 1, before the spell's own
    onset (y < the onset's year), y no later than the panel's common end, with pi(y-1) readable and below 10. A year whose
    pi(y-1) cannot be read is not at risk and is counted apart (``years_pi_unreadable``). A spell with no support yes
    and none unreadable is not strained (``spells_no_support``); one with none yes and one or more unreadable is left out
    and counted (``spells_left_out_supports``, R5); one that broke with no readable onset is left out too.
J6. *Base rate*: a year is "act" if a headline act falls in y-3..y-1; "no act" if none does and every source covers
    y-3..y-1; else "cannot be read". The share is given over all the years (the card's) and over the readable ones.
J7. *Exposure*: exposed if an act falls in the year; neither (left out of the table, counted) if none in the year and
    one in the three before; unexposed if none in y-3..y and every source covers y-3..y; "cannot be read" otherwise
    (counted apart). Past a source's last year an act cannot be read, never "none".
J8. *Censoring (R4)* is read literally: a trial whose y + 3 passes min(the common end, entry + H - 1) is censored, an
    onset seen inside the window or not. Rates are over the uncensored trials; the censored are counted, with how many
    of them show an onset in the observed part of the window.
J9. *The pressure strata* at the end of year Y (reading A: Y = y-1; reading B: Y = y). pi, d and the changes are as the
    panel gives them; the change over k years is v(Y) - v(Y-k) in points; reserves are IFS RAXG_USD at year ends (panel.ifs_levels),
    their 12-month change the end of Y over the end of Y-1 (a fall of 20% or more, or not). d is the IFS end-of-year rate
    against the anchor or the dollar (the market rate under a float, the official rate under a parity: IFS has no other).
    Bins: pi below 5 / 5 to under 10 / 10 or more; d below 5 / 5 to under 15 / 15 or more; changes in pi at most 0 /
    over 0 to 5 / over 5; in d at most 0 / over 0 to 10 / over 10. The market split is panel.split_at at Y, the state in
    default panel.default_at at Y, the regime group (parity, floating) panel.class_at at Y, the decade that of y. Route
    and tercile are the spell's own, as frame c coded them at entry (not re-measured each year: the card says "frame c's
    route and tercile"); supports are the spell's at entry (R5), "one" or "two or more". A value that cannot be read is a
    level of its stratum of its own (``cannot be read``), never dropped.
J10. *The pooled ratio* is Mantel-Haenszel over strata with both sides, risk ratio = sum(a n0 / N) / sum(c n1 / N), a and c the
    onsets of the exposed and the unexposed, n1 and n0 their uncensored trials. It is given twice: one variable at a time
    (the strata are that variable's levels) and jointly (the strata are the cross of every variable), each with the
    number of strata with both sides. No interval, no margin.
J11. *War years apart*: the headline table keeps every trial; beside it, the trials whose year y reads "yes" for a war
    (panel.war_at) are a table of their own, and the others another.
J12. *The dated line's year-before values* read at Y = (the act's year) - 1, as reading A does.

Card C07 (claim 1's second card, parent C04; written after C04's run and its isolated check) adds R6-R12, run by
``build_result_v2`` (``main`` runs C07; C04's run, 59a15b88, stays in git with this file's 3460f3c7):
J13. *A shared money's decision* (R8): a break of a money frame b marks ``shared_or_foreign_money`` yes is keyed by its
    onset month, so the breaks of several members with one onset month count once; a trial's money is shared when frame
    c marks its spell so. The key is the month alone (no union is coded): two unions breaking in one month would merge.
J14. *T2's variants* (R7): from 1960 the headline T2 lines are replaced by the variant's lines (``T2-var-total`` or
    ``T2-var-private``, status apart in the acts list), read as T2 on the headline T2's coverage; before 1960 the
    headline's (Reinhart-Rogoff) lines stay.
J15. *A T2 act inside a default already running* (R7's count): a headline T2 line from 1960 whose year before reads
    "yes" on panel.default_at.
J16. *The base rate's own population* (R10): the breaks whose (money, onset year) is the onset of a strained spell.
"""

from __future__ import annotations

import csv
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
STUDY = HERE.parent
ROOT = STUDY.parents[1]
DATA = ROOT / "data" / "reconstructed"
CARD = STUDY / "cards" / "C04-claim1-dated-lines.yaml"
sys.path.insert(0, str(ROOT / "bank" / "maps" / "FT-001" / "missions" / "code"))

HEADLINE = ("T2", "L1", "L2", "L3", "H1")
L = 3
FROM_YEAR = 1970
AT_RISK_PI_BELOW = 10.0
CANNOT = "cannot be read"
NO_SPELL = "no frame c spell before the onset"

AFTER, SAME, BEFORE, NO_ACT, UNREAD = "after an act", "same year", "before an act", "no act", CANNOT
CLASSES = (AFTER, SAME, BEFORE, NO_ACT, UNREAD)
EXPOSED, UNEXPOSED, NEITHER = "exposed", "unexposed", "neither"
ONSET, NONE, CENSORED = "onset", "none", "censored"

SENTENCE = ("strain and expected inflation are not closed; a ratio above 1 here cannot be read as the effect of an "
            "act.")

PI_LEVELS = ("below 5", "5 to under 10", "10 or more")
D_LEVELS = ("below 5", "5 to under 15", "15 or more")
DPI_LEVELS = ("at most 0", "over 0 to 5", "over 5")
DD_LEVELS = ("at most 0", "over 0 to 10", "over 10")
FALL, NO_FALL = "a fall of 20% or more", "no such fall"
VARIABLES = ("pi", "dpi1", "dpi3", "d", "dd1", "dd3", "split", "reserves", "route", "tercile", "default", "supports",
             "regime", "decade")


# --- reading the files -------------------------------------------------------------------------------------------

def read_csv(path: Path) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def year_of(label) -> int | None:
    """The year of 'YYYY', 'YYYY-MM' or 'YYYY-MM-DD'; None for an empty or unreadable label."""
    s = str(label or "").strip()
    return int(s[:4]) if len(s) >= 4 and s[:4].isdigit() else None


def date_key(label) -> tuple[int, int]:
    """(year, month) of a label, month 0 at year precision; the sort key of time order."""
    s = str(label or "").strip()
    y = year_of(s)
    month = int(s[5:7]) if len(s) >= 7 and s[5:7].isdigit() else 0
    return (y if y is not None else 9999, month)


def source_label(code: str, source: str) -> str:
    """The act source's short name, the grouping of "by act source" (J2)."""
    s = source.lower()
    if s.startswith("bank of canada"):
        return "T2 | Bank of Canada-Bank of England database"
    if "varieties" in s:
        return "T2 | Reinhart-Rogoff, Varieties of crises"
    if "this time is different" in s:
        return "T2 | Reinhart-Rogoff, This Time Is Different (dummies)"
    if s.startswith("garriga"):
        return f"{code} | Garriga (2025)"
    if s.startswith("ilzetzki"):
        return f"{code} | Ilzetzki-Reinhart-Rogoff chronologies"
    return f"{code} | {source[:40]}"


T2_VARIANT_FROM = 1960


def headline_acts(rows: list[dict], t2_route: str = "T2") -> dict[str, list[dict]]:
    """money -> its headline counted acts (J1), in time order; ``t2_route`` a T2 variant read as T2 from 1960 (J14)."""
    out: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        code = r["route"]
        year = year_of(r["entry_date"])
        if year is None:
            continue
        if t2_route != "T2" and code == t2_route and year >= T2_VARIANT_FROM:
            code = "T2"
        elif r["headline"] != "yes" or r["status"] != "counted" or code not in HEADLINE:
            continue
        elif t2_route != "T2" and code == "T2" and year >= T2_VARIANT_FROM:
            continue
        out[r["money"]].append({"code": code, "year": year, "date": r["entry_date"], "source": r["source"],
                                "group": source_label(code, r["source"])})
    for v in out.values():
        v.sort(key=lambda a: (date_key(a["date"]), a["code"]))
    return out


def build_coverage(rows: list[dict]) -> dict[str, dict[str, dict[str, list[tuple[int, int]]]]]:
    """money -> {'by_code': {code: [(first, last)]}, 'by_group': {group: [(first, last)]}} (J2)."""
    out: dict = {}
    for r in rows:
        code = r["act"].split()[0] if r["act"].strip() else ""
        if code not in HEADLINE:
            continue
        try:
            span = (int(r["first_year"]), int(r["last_year"]))
        except ValueError:
            continue
        m = out.setdefault(r["money"], {"by_code": {}, "by_group": {}})
        m["by_code"].setdefault(code, []).append(span)
        m["by_group"].setdefault(source_label(code, r["source"]), []).append(span)
    return out


def covers(intervals: list[tuple[int, int]], first: int, last: int) -> bool:
    """True if the union of the inclusive intervals holds every year of first..last."""
    merged: list[list[int]] = []
    for a, b in sorted(intervals):
        if merged and a <= merged[-1][1] + 1:
            merged[-1][1] = max(merged[-1][1], b)
        else:
            merged.append([a, b])
    return any(a <= first and last <= b for a, b in merged)


def window_readable(cov: dict[str, list[tuple[int, int]]], keys, first: int, last: int) -> bool:
    """Every key's source covers every year of first..last (a key with no interval covers none)."""
    return all(covers(cov.get(k, []), first, last) for k in keys)


# --- R3: the described shares ------------------------------------------------------------------------------------

def classify_break(y: int | None, act_years, readable: bool, span: int = L) -> str:
    """R3, in priority order. ``readable``: every act source covers y-span..y+span. No onset year: cannot be read (J3)."""
    if y is None:
        return UNREAD
    years = set(act_years)
    if any(y - span <= a <= y - 1 for a in years):
        return AFTER
    if y in years:
        return SAME
    if any(y + 1 <= a <= y + span for a in years):
        return BEFORE
    return NO_ACT if readable else UNREAD


def share_table(classes: list[str]) -> dict:
    n = len(classes)
    readable = n - classes.count(UNREAD)
    return {"n": n, "readable": readable,
            **{c: {"n": classes.count(c), "share": (classes.count(c) / n if n else None),
                   **({"share_of_readable": classes.count(c) / readable if readable else None} if c != UNREAD else {})}
               for c in CLASSES}}


def break_classes(breaks: list[dict], acts: dict[str, list[dict]], keys_of, act_key) -> list[str]:
    """Each break's class (R3) over the acts ``act_key`` keeps; ``keys_of(money) -> (coverage intervals by key, keys)``
    names the sources whose coverage of y-3..y+3 decides "no act" from "cannot be read"."""
    out = []
    for b in breaks:
        y = b["onset_year"]
        years = [a["year"] for a in acts.get(b["money"], []) if act_key(a)]
        cov, keys = keys_of(b["money"])
        readable = y is not None and window_readable(cov, keys, y - L, y + L)
        out.append(classify_break(y, years, readable))
    return out


def shares(breaks: list[dict], acts: dict, coverage: dict) -> dict:
    def by_code(codes):
        return lambda m: (coverage.get(m, {}).get("by_code", {}), codes)
    out = {"overall": share_table(break_classes(breaks, acts, by_code(HEADLINE), lambda a: True))}
    nT2 = tuple(c for c in HEADLINE if c != "T2")
    out["without_T2"] = share_table(break_classes(breaks, acts, by_code(nT2), lambda a: a["code"] != "T2"))
    out["onset_unreadable"] = sum(1 for b in breaks if b["onset_year"] is None)
    groups = sorted({a["group"] for v in acts.values() for a in v} |
                    {g for c in coverage.values() for g in c["by_group"]})
    by_source = {}
    for g in groups:
        def keys_of(m, g=g):
            return coverage.get(m, {}).get("by_group", {}), (g,)
        covered = sum(1 for b in breaks if b["onset_year"] is not None and
                      covers(coverage.get(b["money"], {}).get("by_group", {}).get(g, []),
                             b["onset_year"] - L, b["onset_year"] + L))
        if not covered and not any(a["group"] == g for b in breaks for a in acts.get(b["money"], [])
                                   if b["onset_year"] is not None and abs(a["year"] - b["onset_year"]) <= L):
            by_source[g] = {"windows_covered": 0, "note": "no window from 1970 is read by this source"}   # R12
            continue
        table = share_table(break_classes(breaks, acts, keys_of, lambda a, g=g: a["group"] == g))
        table["windows_covered"] = covered
        by_source[g] = table
    out["by_act_source"] = by_source
    return out


# --- the dated lines ---------------------------------------------------------------------------------------------

def fmt(v) -> object:
    return CANNOT if v is None else round(float(v), 2)


def year_before_values(reader, money: str, act_year: int) -> dict:
    y = act_year - 1
    return {"pi": fmt(reader.pi(money, y)), "d": fmt(reader.d(money, y)),
            "reserves_12m_change": fmt(reader.reserves_change(money, y)), "market_split": reader.split(money, y),
            "war": reader.war(money, y)}


def frame_c_spell(spells: list[dict], year: int) -> dict | str:
    """R1: the money's last counted spell entered at or before ``year``, else the said text."""
    before = [s for s in spells if s["entry"] <= year]
    if not before:
        return NO_SPELL
    s = max(before, key=lambda s: s["entry"])
    return {"entry": s["entry"], "route": s["route"], "tercile": s["tercile"]}


def build_line(brk: dict, spells: list[dict], acts: list[dict], reader, after_crossing: bool = False) -> dict:
    """One break's dated line (R2): the acts from onset year - 3 (J3: crossing year - 3 without an onset) to the
    crossing, each with its year-before values; ``after_crossing`` (C07's R11): also the acts after the crossing up to
    the onset's year + 3, marked."""
    cross = brk["crossing_year"]
    anchor = brk["onset_year"] if brk["onset_year"] is not None else cross
    last = max(cross, anchor + L) if after_crossing else cross
    listed = [a for a in acts if anchor - L <= a["year"] <= last]
    cache: dict[int, dict] = {}
    out_acts = []
    for a in listed:
        if a["year"] not in cache:
            cache[a["year"]] = year_before_values(reader, brk["money"], a["year"])
        out_acts.append({"act": a["code"], "date": a["date"], "source": a["source"], "year_before": cache[a["year"]],
                         **({"after_the_crossing": True} if a["year"] > cross else {})})
    return {"money": brk["money"], "crossing": brk["crossing"],
            "onset": brk["onset"] if brk["onset_year"] is not None else CANNOT, "onset_route": brk["onset_route"],
            "frame_c": frame_c_spell(spells, anchor), "acts": out_acts}


def prepare_breaks(rows: list[dict], monies_with_spells: set[str], from_year: int = FROM_YEAR) -> list[dict]:
    """Frame b's counted lines, crossing from ``from_year``, money with a counted frame c spell, in time order."""
    out = []
    for r in rows:
        cross = year_of(r["entry_date"])
        if r["status"] != "counted" or cross is None or cross < from_year or r["money"] not in monies_with_spells:
            continue
        onset = (r.get("break_onset") or "").strip()
        oy = year_of(onset) if onset != CANNOT else None
        out.append({"money": r["money"], "crossing": r["entry_date"], "crossing_year": cross,
                    "onset": onset, "onset_year": oy, "onset_route": r.get("onset_route") or CANNOT,
                    "shared": r.get("shared_or_foreign_money") == "yes"})
    out.sort(key=lambda b: (date_key(b["crossing"]), b["money"]))
    return out


# --- the spells, the at-risk years, the trials -------------------------------------------------------------------

SUPPORT_COLUMNS = ("taken_back", "limit_by_rule", "limit_by_institution", "force")


def supports_state(row: dict) -> str:
    """R5: 'two or more' / 'one' (counting the yes), 'none' (all four read no), or 'cannot be read' (none yes and one or
    more unread: the spell is left out)."""
    vals = [row.get(k, CANNOT) for k in SUPPORT_COLUMNS]
    yes = sum(v == "yes" for v in vals)
    if yes >= 2:
        return "two or more"
    if yes == 1:
        return "one"
    return CANNOT if any(v != "no" for v in vals) else "none"


def prepare_spells(rows: list[dict]) -> tuple[list[dict], dict]:
    """The strained spells (J5) and what is left out, counted apart. ``all_counted`` keeps every counted spell for R1."""
    spells, out = [], {"spells_left_out_supports": 0, "spells_no_support": 0, "spells_left_out_onset": 0}
    all_counted = []
    for r in rows:
        if r["status"] != "counted":
            continue
        entry = year_of(r["entry_date"])
        broke = r["outcome"] in ("broke", "broke and restored")
        onset = year_of(r["onset_date"]) if broke else None
        base = {"money": r["money"], "entry": entry, "H": int(r["H"]), "route": r["route"],
                "tercile": r["tercile"] or CANNOT, "onset_year": onset,
                "onset_month": str(r.get("onset_date") or "")[:7] if broke else "",
                "shared": r.get("shared_or_foreign_money") == "yes"}
        all_counted.append(base)
        sup = supports_state(r)
        if sup == CANNOT:
            out["spells_left_out_supports"] += 1
        elif sup == "none":
            out["spells_no_support"] += 1
        elif broke and onset is None:
            out["spells_left_out_onset"] += 1
        else:
            spells.append({**base, "supports": sup})
    out["all_counted"] = all_counted
    return spells, out


def at_risk_years(entry: int, H: int, onset_year: int | None, pi_of, end: int, from_year: int = FROM_YEAR,
                  pi_below: float = AT_RISK_PI_BELOW) -> tuple[list[int], int]:
    """J5: (the at-risk years, the years left out because pi(y-1) cannot be read)."""
    stop = min(entry + H - 1, end)
    if onset_year is not None:
        stop = min(stop, onset_year - 1)
    years, unread = [], 0
    for y in range(max(entry, from_year), stop + 1):
        p = pi_of(y - 1)
        if p is None:
            unread += 1
        elif p < pi_below:
            years.append(y)
    return years, unread


def exposure(y: int, act_years, readable: bool, span: int = L) -> str:
    """J7: exposed (an act in y), neither (none in y, one in y-3..y-1), unexposed (none in y-3..y, sources cover), else
    cannot be read. ``readable``: every source covers y-3..y."""
    years = set(act_years)
    if y in years:
        return EXPOSED
    if any(y - span <= a <= y - 1 for a in years):
        return NEITHER
    return UNEXPOSED if readable else UNREAD


def forward_outcome(y: int, onset_year: int | None, last_observed: int, span: int = L) -> tuple[str, bool]:
    """R4 (J8): (onset / none / censored, whether a censored trial shows an onset in the observed part of its window)."""
    if y + span > last_observed:
        seen = onset_year is not None and y + 1 <= onset_year <= min(y + span, last_observed)
        return CENSORED, seen
    if onset_year is not None and y + 1 <= onset_year <= y + span:
        return ONSET, False
    return NONE, False


def bin_below(v, cuts: tuple[float, float], labels: tuple[str, str, str]) -> str:
    """v < c0, c0 <= v < c1, v >= c1."""
    if v is None:
        return CANNOT
    return labels[0] if v < cuts[0] else (labels[1] if v < cuts[1] else labels[2])


def bin_above(v, cuts: tuple[float, float], labels: tuple[str, str, str]) -> str:
    """v <= c0, c0 < v <= c1, v > c1."""
    if v is None:
        return CANNOT
    return labels[0] if v <= cuts[0] else (labels[1] if v <= cuts[1] else labels[2])


def pi_bin(v):
    return bin_below(v, (5, 10), PI_LEVELS)


def d_bin(v):
    return bin_below(v, (5, 15), D_LEVELS)


def delta(a, b):
    return None if a is None or b is None else a - b


def reserves_bin(change) -> str:
    return CANNOT if change is None else (FALL if change <= -20 else NO_FALL)


def trial_strata(spell: dict, y: int, Y: int, reader) -> dict:
    """The pressure strata of one trial measured to the end of year Y (J9; reading A: Y = y-1, B: Y = y)."""
    m = spell["money"]
    p, d = reader.pi(m, Y), reader.d(m, Y)
    return {"pi": pi_bin(p), "dpi1": bin_above(delta(p, reader.pi(m, Y - 1)), (0, 5), DPI_LEVELS),
            "dpi3": bin_above(delta(p, reader.pi(m, Y - 3)), (0, 5), DPI_LEVELS), "d": d_bin(d),
            "dd1": bin_above(delta(d, reader.d(m, Y - 1)), (0, 10), DD_LEVELS),
            "dd3": bin_above(delta(d, reader.d(m, Y - 3)), (0, 10), DD_LEVELS),
            "split": reader.split(m, Y), "reserves": reserves_bin(reader.reserves_change(m, Y)),
            "route": spell["route"], "tercile": spell["tercile"], "default": reader.default(m, Y),
            "supports": spell["supports"], "regime": reader.regime(m, Y), "decade": f"{y // 10 * 10}s"}


def build_trials(spells: list[dict], reader, end: int, from_year: int = FROM_YEAR) -> tuple[list[dict], dict]:
    """Every at-risk year as a trial with both readings' strata, its war year and its observation limit."""
    trials, unread_total = [], 0
    for s in spells:
        years, unread = at_risk_years(s["entry"], s["H"], s["onset_year"], lambda y, m=s["money"]: reader.pi(m, y),
                                      end, from_year)
        unread_total += unread
        for y in years:
            trials.append({"money": s["money"], "entry": s["entry"], "y": y, "onset_year": s["onset_year"],
                           "decision": decision_key(s["money"], s.get("shared", False), s["onset_year"],
                                                    s.get("onset_month", "")),
                           "last_observed": min(end, s["entry"] + s["H"] - 1), "war": reader.war(s["money"], y),
                           "A": trial_strata(s, y, y - 1, reader), "B": trial_strata(s, y, y, reader)})
    return trials, {"years_pi_unreadable": unread_total}


# --- the base rate -----------------------------------------------------------------------------------------------

def act_filter(acts: dict, money: str, codes) -> list[int]:
    return [a["year"] for a in acts.get(money, []) if a["code"] in codes]


def base_rate_year(y: int, act_years, readable: bool, span: int = L) -> str:
    """J6: 'act' (one in y-3..y-1), 'no act' (none, sources cover) or 'cannot be read'."""
    if any(y - span <= a <= y - 1 for a in act_years):
        return "act"
    return NO_ACT if readable else UNREAD


def base_rate(trials: list[dict], acts: dict, coverage: dict) -> dict:
    out = {}
    for name, codes in (("overall", HEADLINE), ("without_T2", tuple(c for c in HEADLINE if c != "T2"))):
        marks = []
        for t in trials:
            cov = coverage.get(t["money"], {}).get("by_code", {})
            marks.append(base_rate_year(t["y"], act_filter(acts, t["money"], codes),
                                        window_readable(cov, codes, t["y"] - L, t["y"] - 1)))
        n = len(marks)
        a, none, un = marks.count("act"), marks.count(NO_ACT), marks.count(UNREAD)
        out[name] = {"years": n, "with_act": a, "share": a / n if n else None, "no_act": none, "cannot_be_read": un,
                     "share_of_readable": a / (a + none) if a + none else None}
    return out


# --- the forward table -------------------------------------------------------------------------------------------

def decision_key(money: str, shared: bool, onset_year, onset_month: str = "") -> tuple:
    """J13: a break's key; a shared money's break is keyed by its onset month alone."""
    if shared and onset_month:
        return ("shared", onset_month)
    return (money, onset_year)


def new_cell() -> dict:
    return {"trials": 0, "censored": 0, "censored_onset_seen": 0, "n": 0, "onsets": 0}


def add_trial(cell: dict, outcome: str, seen: bool, brk: tuple | None = None, decision: tuple | None = None) -> None:
    cell["trials"] += 1
    if outcome == CENSORED:
        cell["censored"] += 1
        cell["censored_onset_seen"] += int(seen)
    else:
        cell["n"] += 1
        cell["onsets"] += int(outcome == ONSET)
        if outcome == ONSET and brk is not None:          # R9: the distinct breaks behind the trial-years
            cell.setdefault("_breaks", set()).add(brk)
            cell.setdefault("_decisions", set()).add(decision or brk)


def finish_cell(cell: dict) -> dict:
    out = {k: v for k, v in cell.items() if not k.startswith("_")}
    if "_breaks" in cell or "onsets" in cell:
        out["distinct_breaks"] = len(cell.get("_breaks", ()))
        out["distinct_decisions"] = len(cell.get("_decisions", ()))
    return {**out, "rate": cell["onsets"] / cell["n"] if cell["n"] else None}


def cells_by(items: list[tuple], keyfn) -> dict:
    """items: (exposure, outcome, seen, strata[, break, decision]). -> {key: {'exposed': cell, 'unexposed': cell}}."""
    out: dict = {}
    for item in items:
        expo, outcome, seen, strata = item[:4]
        brk, decision = (item[4], item[5]) if len(item) > 5 else (None, None)
        cell = out.setdefault(keyfn(strata), {EXPOSED: new_cell(), UNEXPOSED: new_cell()})
        add_trial(cell[expo], outcome, seen, brk, decision)
    return out


def mantel_haenszel(cells: dict) -> dict:
    """J10: the pooled risk ratio over the strata with both sides (uncensored trials on each)."""
    num = den = 0.0
    both = 0
    onsets = [0, 0]
    for cell in cells.values():
        e, u = cell[EXPOSED], cell[UNEXPOSED]
        if not e["n"] or not u["n"]:
            continue
        n = e["n"] + u["n"]
        both += 1
        num += e["onsets"] * u["n"] / n
        den += u["onsets"] * e["n"] / n
        onsets[0] += e["onsets"]
        onsets[1] += u["onsets"]
    out = {"strata_with_both_sides": both, "onsets_exposed_there": onsets[0], "onsets_unexposed_there": onsets[1],
           "risk_ratio": num / den if den else None}
    if not both:
        out["note"] = "no stratum has both sides: counts only, no ratio"
    elif not den and not onsets[0]:
        out["note"] = "no onset on either side in the strata with both sides: no ratio"
    elif not den:
        out["note"] = "no onset among the unexposed in the strata with both sides: no ratio"
    elif not num:
        out["note"] = "no onset among the exposed in the strata with both sides"
    return out


def table_of(items: list[tuple]) -> dict:
    """One variant's table: totals, each variable's levels with the pooled ratio over them, the joint ratio."""
    total = cells_by(items, lambda s: "all")["all"] if items else {EXPOSED: new_cell(), UNEXPOSED: new_cell()}
    e, u = finish_cell(total[EXPOSED]), finish_cell(total[UNEXPOSED])
    out = {"exposed": e, "unexposed": u,
           "crude_ratio": (e["rate"] / u["rate"]) if e["rate"] is not None and u["rate"] else None}
    by_var = {}
    for v in VARIABLES:
        cells = cells_by(items, lambda s, v=v: s[v])
        by_var[v] = {"levels": {k: {EXPOSED: finish_cell(c[EXPOSED]), UNEXPOSED: finish_cell(c[UNEXPOSED])}
                                for k, c in sorted(cells.items())}, **mantel_haenszel(cells)}
    out["by_variable"] = by_var
    joint = cells_by(items, lambda s: tuple(s[v] for v in VARIABLES))
    out["joint"] = {"strata": len(joint), **mantel_haenszel(joint),
                    "strata_with_both_sides_listed": [
                        {"stratum": dict(zip(VARIABLES, k)), EXPOSED: finish_cell(c[EXPOSED]),
                         UNEXPOSED: finish_cell(c[UNEXPOSED])}
                        for k, c in sorted(joint.items()) if c[EXPOSED]["n"] and c[UNEXPOSED]["n"]]}
    return out


def variant_items(trials: list[dict], acts: dict, coverage: dict, codes, reading: str, war_keep=None) -> tuple:
    """(items for the table, counts of the trials left out: neither / cannot be read)."""
    items, left = [], {NEITHER: 0, UNREAD: 0}
    for t in trials:
        if war_keep is not None and not war_keep(t["war"]):
            continue
        years = act_filter(acts, t["money"], codes)
        cov = coverage.get(t["money"], {}).get("by_code", {})
        expo = exposure(t["y"], years, window_readable(cov, codes, t["y"] - L, t["y"]))
        if expo in left:
            left[expo] += 1
            continue
        outcome, seen = forward_outcome(t["y"], t["onset_year"], t["last_observed"])
        items.append((expo, outcome, seen, t[reading], (t["money"], t["onset_year"]),
                      t.get("decision", (t["money"], t["onset_year"]))))
    return items, left


def forward_table(trials: list[dict], acts: dict, coverage: dict) -> dict:
    nT2 = tuple(c for c in HEADLINE if c != "T2")
    variants = [("all trials", HEADLINE, None), ("without T2", nT2, None)]
    variants += [(f"{c} alone", (c,), None) for c in HEADLINE]
    variants += [("war years apart: no war year in y", HEADLINE, lambda w: w != "yes"),
                 ("war years apart: a war year in y", HEADLINE, lambda w: w == "yes")]
    out = {}
    for reading in ("A", "B"):
        out[reading] = {}
        for name, codes, war_keep in variants:
            items, left = variant_items(trials, acts, coverage, codes, reading, war_keep)
            out[reading][name] = {"trials_left_out": left, **table_of(items)}
    return out


def no_war(w: str) -> bool:
    return w != "yes"


def forward_table_v2(trials: list[dict], acts: dict, coverage: dict, full: bool = True) -> dict:
    """R6: the headline is the trials with no war year in y (a war year that cannot be read stays in, counted); the war
    years beside; C04's all-trials table as a variant. ``full``: also without T2 and each act alone."""
    nT2 = tuple(c for c in HEADLINE if c != "T2")
    variants = [("headline: no war year in y", HEADLINE, no_war)]
    if full:
        variants += [("without T2", nT2, no_war)] + [(f"{c} alone", (c,), no_war) for c in HEADLINE]
    variants += [("a war year in y", HEADLINE, lambda w: w == "yes"), ("all trials (C04's headline)", HEADLINE, None)]
    out = {}
    for reading in ("A", "B"):
        out[reading] = {}
        for name, codes, war_keep in variants:
            items, left = variant_items(trials, acts, coverage, codes, reading, war_keep)
            table = table_of(items)
            if not (full and name.startswith("headline")):
                table["joint"].pop("strata_with_both_sides_listed", None)
            out[reading][name] = {"trials_left_out": left, **table}
        out[reading]["war_unreadable_in_headline"] = sum(1 for t in trials if t["war"] not in ("yes", "no"))
    return out


def shared_once(breaks: list[dict]) -> list[dict]:
    """R8 (J13): the breaks with a shared money's breaks of one onset month kept once (the first in time order)."""
    seen, out = set(), []
    for b in breaks:
        key = decision_key(b["money"], b.get("shared", False), b["onset_year"], (b.get("onset") or "")[:7])
        if key in seen:
            continue
        seen.add(key)
        out.append(b)
    return out


def t2_inside_default(acts_rows: list[dict], reader) -> dict:
    """J15: the headline T2 lines from 1960, and those whose year before already reads a stock in default."""
    lines = [(r["money"], year_of(r["entry_date"])) for r in acts_rows if r["route"] == "T2" and r["headline"] == "yes"
             and r["status"] == "counted" and (year_of(r["entry_date"]) or 0) >= T2_VARIANT_FROM]
    inside = sum(1 for m, y in lines if reader.default(m, y - 1) == "yes")
    return {"t2_lines_from_1960": len(lines), "inside_a_running_default": inside}


def analysis(breaks: list[dict], trials: list[dict], acts: dict, coverage: dict, population: set, full: bool) -> dict:
    out = {"shares": shares(breaks, acts, coverage),
           "shares_shared_once": shares(shared_once(breaks), acts, coverage)}
    pop = [b for b in breaks if (b["money"], b["onset_year"]) in population]
    out["shares_base_rate_population"] = {"breaks": len(pop), **shares(pop, acts, coverage)}
    out["base_rate"] = base_rate(trials, acts, coverage)
    out["forward_table"] = forward_table_v2(trials, acts, coverage, full)
    if not full:
        out["shares"].pop("by_act_source", None)
        out["shares_shared_once"].pop("by_act_source", None)
        out["shares_base_rate_population"].pop("by_act_source", None)
    return out


def build_result_v2(frame_b: list[dict], frame_c: list[dict], acts_rows: list[dict], coverage_rows: list[dict],
                    reader, end: int) -> dict:
    """Card C07: C04's build with R6-R12."""
    coverage = build_coverage(coverage_rows)
    spells, left = prepare_spells(frame_c)
    all_counted = left.pop("all_counted")
    by_money: dict[str, list[dict]] = defaultdict(list)
    for s_ in all_counted:
        by_money[s_["money"]].append(s_)
    breaks = prepare_breaks(frame_b, set(by_money))
    acts = headline_acts(acts_rows)
    lines = [build_line(b, by_money[b["money"]], acts.get(b["money"], []), reader, after_crossing=True)
             for b in breaks]
    trials, trial_counts = build_trials(spells, reader, end)
    population = {(s_["money"], s_["onset_year"]) for s_ in spells if s_["onset_year"] is not None}
    readings = {"headline": analysis(breaks, trials, acts, coverage, population, full=True)}
    for route in ("T2-var-total", "T2-var-private"):
        readings[route] = analysis(breaks, trials, headline_acts(acts_rows, route), coverage, population, full=False)
    return {
        "common_end": end,
        "parameters": {"from_year": FROM_YEAR, "L_years": L, "at_risk_pi_below": AT_RISK_PI_BELOW,
                       "acts": list(HEADLINE), "t2_readings": ["headline", "T2-var-total", "T2-var-private"],
                       "not_run": ["F1", "W1"]},
        "breaks": len(breaks),
        "breaks_shared_once": len(shared_once(breaks)),
        "breaks_of_shared_monies": sum(b["shared"] for b in breaks),
        "lines": lines,
        "t2": t2_inside_default(acts_rows, reader),
        "spells": {"spells_strained": len(spells), **left, **trial_counts,
                   "trials": len(trials), "spells_broke": len(population)},
        "readings": readings,
        "said": ["R1 compares years: a spell entered in the onset's year counts as at or before it",
                 "the market split and the regime at Y read the class of Y-1",
                 "R4 censors every trial in a spell's last three years, counted in each cell"],
        "sentence": SENTENCE,
    }


# --- the build ---------------------------------------------------------------------------------------------------

def build_result(frame_b: list[dict], frame_c: list[dict], acts_rows: list[dict], coverage_rows: list[dict],
                 reader, end: int) -> dict:
    acts, coverage = headline_acts(acts_rows), build_coverage(coverage_rows)
    spells, left = prepare_spells(frame_c)
    all_counted = left.pop("all_counted")
    by_money: dict[str, list[dict]] = defaultdict(list)
    for s in all_counted:
        by_money[s["money"]].append(s)
    breaks = prepare_breaks(frame_b, set(by_money))
    lines = [build_line(b, by_money[b["money"]], acts.get(b["money"], []), reader) for b in breaks]
    trials, trial_counts = build_trials(spells, reader, end)
    return {
        "common_end": end,
        "parameters": {"from_year": FROM_YEAR, "L_years": L, "at_risk_pi_below": AT_RISK_PI_BELOW,
                       "acts": list(HEADLINE), "not_run": ["F1", "W1"]},
        "breaks": len(breaks),
        "lines": lines,
        "shares": shares(breaks, acts, coverage),
        "base_rate": {**base_rate(trials, acts, coverage), "spells_strained": len(spells), **left, **trial_counts},
        "forward_table": forward_table(trials, acts, coverage),
        "sentence": SENTENCE,
    }


# --- the panel's readers, one reader for every year-level reading -----------------------------------------------

class PanelReader:
    """The annual readings frame c uses, through the panel's own readers (panel.py, strain.Readings's sources)."""

    def __init__(self) -> None:
        import panel
        self.P = panel
        self.pan = panel.Panel()
        self.end = panel.common_end(self.pan.have_annual(), 1)
        self.reserves = panel.ifs_levels("RAXG_USD")
        self.irr = panel.irr_classes()
        self._pi: dict[str, dict[int, float]] = {}
        self._d: dict[str, dict[int, float]] = {}
        self._war: dict[tuple, str] = {}

    def pi(self, m: str, y: int):
        if m not in self._pi:
            self._pi[m] = ({yy: v for yy, (v, _, _) in self.pan.pi_annual(m).items()} if m in self.pan.monies else {})
        return self._pi[m].get(y)

    def d(self, m: str, y: int):
        if m not in self._d:
            self._d[m] = ({yy: v[0] for yy, v in self.pan.d_annual(m).items()} if m in self.pan.monies else {})
        return self._d[m].get(y)

    def reserves_change(self, m: str, y: int):
        lv = self.reserves.get(m, {})
        if y in lv and y - 1 in lv and lv[y - 1] > 0:
            return 100 * (lv[y] / lv[y - 1] - 1)
        return None

    def split(self, m: str, y: int) -> str:
        return self.P.split_at(m, str(y))

    def default(self, m: str, y: int) -> str:
        return self.P.default_at(m, y)

    def regime(self, m: str, y: int) -> str:
        cls, _ = self.P.class_at(self.irr.get(m), y)
        return self.P.regime_group(cls)

    def war(self, m: str, y: int) -> str:
        if (m, y) not in self._war:
            self._war[(m, y)] = self.P.war_at(m, y)
        return self._war[(m, y)]


def run(data: Path = DATA, reader=None) -> dict:
    reader = reader or PanelReader()
    return build_result(read_csv(data / "ft001-b" / "series.csv"), read_csv(data / "ft001-c" / "series.csv"),
                        read_csv(data / "ft001-acts" / "series.csv"), read_csv(data / "ft001-acts" / "coverage.csv"),
                        reader, reader.end)


CARD_V2 = STUDY / "cards" / "C07-claim1-dated-lines-v2.yaml"


def run_v2(data: Path = DATA, reader=None) -> dict:
    reader = reader or PanelReader()
    return build_result_v2(read_csv(data / "ft001-b" / "series.csv"), read_csv(data / "ft001-c" / "series.csv"),
                           read_csv(data / "ft001-acts" / "series.csv"),
                           read_csv(data / "ft001-acts" / "coverage.csv"), reader, reader.end)


CARD_V3 = STUDY / "cards" / "C15-claim1-institution-m0.yaml"


def m0_frame_c(rows: list[dict]) -> list[dict]:
    """C15: frame c's lines with the limit by institution read by M0's text (claim2's reader, C13's), every other
    column as built. Refuses unless the reader first reproduces frame c's columns on every counted line."""
    import claim2
    inp = claim2.Inputs()
    counted = [r for r in rows if r["status"] == "counted"]
    bad = claim2.reproduces(counted, inp)
    if bad:
        raise ValueError(f"frame c's supports not reproduced ({len(bad)}): {bad[:5]}")
    new = iter(claim2.reread(counted, inp))
    return [next(new) if r["status"] == "counted" else r for r in rows]


def run_v3(data: Path = DATA, reader=None) -> dict:
    """C15: C07 as it runs, on frame c's lines re-read by M0's text."""
    reader = reader or PanelReader()
    frame_c = m0_frame_c(read_csv(data / "ft001-c" / "series.csv"))
    return build_result_v2(read_csv(data / "ft001-b" / "series.csv"), frame_c,
                           read_csv(data / "ft001-acts" / "series.csv"),
                           read_csv(data / "ft001-acts" / "coverage.csv"), reader, reader.end)


def main(card: Path = CARD_V3) -> Path:
    """Runs C15 (the default), C07 given its path, or C04 as it ran given C04's."""
    from ft import cards
    cards.require_locked(card)
    result = run() if card == CARD else run_v2() if card == CARD_V2 else run_v3()
    return cards.write_result(STUDY, card, result)


if __name__ == "__main__":
    print(main())
