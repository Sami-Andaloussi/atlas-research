"""Claim 2 (card C05): under the same strain, did monies with more supports standing hold more often?

M0 v4.2 section 6 as the card writes it: frame c's counted spells from 1970; "held" against "broke" or "broke and
restored"; two or more supports against one or none; the Mantel-Haenszel difference in the share held over the
strata route x tercile x era x default at entry; a 90% percentile interval from 2,000 bootstrap draws over monies;
margin 10 points, floor 20 spells a side. From the study's folder::

    ../../toolkit/bin/ftpy code/claim2.py

Readings made in code, in the open (the card's own are C05-R1):

K1. *A war year inside H* (the variant "war in H out"): frame c's ``war_years_in_H`` reads "n" or "n (+k unreadable)";
    a spell is left out when n >= 1. Unreadable war years do not take a spell out (they are counted in G05's
    variants instead).
K2. *Each support alone*: "yes" against "no"; "cannot be read" is in neither side. Printed with the same statistic,
    with no verdict of its own.
"""

from __future__ import annotations

import csv
import math
import re
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
STUDY = HERE.parent
ROOT = STUDY.parents[1]
FRAME_C = ROOT / "data" / "reconstructed" / "ft001-c"
CARD = STUDY / "cards" / "C05-claim2-supports.yaml"
CARD_CFA = STUDY / "cards" / "C11-claim2-cfa-out.yaml"
CARD_M0 = STUDY / "cards" / "C13-claim2-institution-m0.yaml"
FRAME_A = ROOT / "data" / "reconstructed" / "ft001-a"
sys.path.insert(0, str(ROOT / "bank" / "maps" / "FT-001" / "missions" / "code"))

TWO, FEWER = "two or more", "one or none"
STRATA = ("route", "tercile", "era", "default_at_entry")


def counted(rows: list[dict], from_year: int = 1970) -> list[dict]:
    return [r for r in rows if r["status"] == "counted" and int(str(r["entry_date"])[:4]) >= from_year]


def side_of(row: dict, key: str) -> int | None:
    """1 for the side with more supports (or "yes" for one support alone), 0 for the other, None if unread."""
    v = row.get(key, "")
    if v in (TWO, "yes"):
        return 1
    if v in (FEWER, "no"):
        return 0
    return None


def held(row: dict) -> int:
    return 1 if row["outcome"] == "held" else 0


def strata(rows: list[dict], key: str) -> dict[tuple, list[list[int]]]:
    """Each stratum's held outcomes per side: {stratum: [[side 0 outcomes], [side 1 outcomes]]}. A line whose default
    at entry cannot be read is in no stratum (N3)."""
    out: dict[tuple, list[list[int]]] = defaultdict(lambda: [[], []])
    for r in rows:
        s = side_of(r, key)
        if s is None or r["default_at_entry"] not in ("yes", "no"):
            continue
        out[tuple(str(r[k]) for k in STRATA)][s].append(held(r))
    return out


def mh_difference(st: dict[tuple, list[list[int]]]) -> tuple[float | None, list[int], int]:
    """(D in points, [n one or none, n two or more] in strata with both sides, strata with both sides)."""
    num = den = 0.0
    n = [0, 0]
    both = 0
    for s0, s1 in st.values():
        if not s0 or not s1:
            continue
        both += 1
        n[0] += len(s0)
        n[1] += len(s1)
        w = len(s0) * len(s1) / (len(s0) + len(s1))
        num += w * (sum(s1) / len(s1) - sum(s0) / len(s0))
        den += w
    return (100 * num / den if den else None), n, both


def bootstrap(rows: list[dict], key: str, draws: int = 2000, seed: int = 1797, level: float = 0.90
              ) -> tuple[float | None, float | None, int]:
    """(lower, upper, dropped draws): monies drawn with replacement, each with all its spells."""
    by_money: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        by_money[r["money"]].append(r)
    monies = sorted(by_money)
    rng = np.random.default_rng(seed)
    got, dropped = [], 0
    for _ in range(draws):
        pick = rng.integers(0, len(monies), len(monies))
        sample = [r for i in pick for r in by_money[monies[i]]]
        d, _, both = mh_difference(strata(sample, key))
        if d is None or not both:
            dropped += 1
            continue
        got.append(d)
    if not got:
        return None, None, dropped
    lo, hi = np.quantile(got, [(1 - level) / 2, 1 - (1 - level) / 2])
    return float(lo), float(hi), dropped


def verdict(d: float | None, lo: float | None, hi: float | None, n: list[int], margin: float = 10,
            floor: int = 20) -> str:
    if d is None or min(n) < floor:
        return "too thin"
    if d >= margin and lo is not None and lo > 0:
        return "confirmed"
    if hi is not None and hi < margin:
        return "refuted"
    return "we cannot conclude"


def reading(rows: list[dict], key: str, draws: int = 2000, seed: int = 1797) -> dict:
    import strain
    st = strata(rows, key)
    d, n, both = mh_difference(st)
    lo, hi, dropped = bootstrap(rows, key, draws, seed) if d is not None else (None, None, draws)
    mde = strain.claim2_mde(rows, key) if key.startswith("supports_count") else None
    return {"separator": key, "D_points": d, "interval_90": [lo, hi], "n_one_or_none": n[0], "n_two_or_more": n[1],
            "strata_with_both_sides": both, "dropped_draws": dropped, "mde_points": mde and mde["mde_points"],
            "outcome": verdict(d, lo, hi, n)}


def war_in_h(row: dict) -> bool:
    """K1: at least one war year read inside H."""
    head = str(row.get("war_years_in_H", "0")).split()[0]
    return head.isdigit() and int(head) >= 1


def claim_verdict(head: str, without_tb: str, without_pegs: str) -> str:
    """The claim's verdict (C05-R1): the headline's; too thin gives 'we cannot conclude (too thin)'; a verdict that
    turns on 'taken back' or on pegs and boards gives 'we cannot conclude'."""
    if head == "too thin":
        return "we cannot conclude (too thin)"
    if head in ("confirmed", "refuted") and (without_tb != head or without_pegs != head):
        return "we cannot conclude (the verdict turns on taken back or on pegs and boards)"
    return head


def read_csv(path: Path) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


VARIANT_FILES = ("regime-carried-out", "war-unreadable-as-no", "war-after-cow-no", "entry-year-counted", "H5", "H20")
SEPARATOR_VARIANTS = ("supports_count_cap_025", "supports_count_cap_075", "supports_count_index_04",
                      "supports_count_index_06", "supports_count_ka_01", "supports_count_ka_05")
SUPPORTS = ("taken_back", "limit_by_rule", "limit_by_institution", "force")
READINGS = ("supports_count", "supports_count_without_taken_back", "supports_count_without_pegs")


def run(frame_c: Path = FRAME_C, draws: int = 2000) -> dict:
    head_rows = counted(read_csv(frame_c / "series.csv"))
    out: dict = {"lines": len(head_rows), "monies": len({r["money"] for r in head_rows})}
    out["readings"] = {k: reading(head_rows, k, draws) for k in READINGS}
    out["claim"] = claim_verdict(*(out["readings"][k]["outcome"] for k in READINGS))
    out["each_support_alone"] = {k: reading(head_rows, k, draws) for k in SUPPORTS}
    no_war = [r for r in head_rows if not war_in_h(r)]
    out["war_in_H_out"] = {"lines": len(no_war), **{k: reading(no_war, k, draws) for k in READINGS}}
    out["frame_c_variants"] = {}
    for name in VARIANT_FILES:
        rows = counted(read_csv(frame_c / f"variant-{name}.csv"))
        out["frame_c_variants"][name] = {"lines": len(rows), **{k: reading(rows, k, draws) for k in READINGS}}
    out["separator_variants"] = {k: reading(head_rows, k, draws) for k in SEPARATOR_VARIANTS}
    for k in READINGS:
        same = [v[k]["outcome"] == out["readings"][k]["outcome"] for v in
                list(out["frame_c_variants"].values()) + [out["war_in_H_out"]]]
        out.setdefault("variants_counted", {})[k] = f"{sum(same)} of {len(same)} variants tell the same outcome"
    return out


def cfa_members(unions: tuple[str, ...] = ("XOF", "XAF")) -> set[str]:
    """C11: the CFA franc unions' member states, in any year, from frame a's union table."""
    import frame_a
    return {m for u in unions for m in frame_a.UNIONS[u][1]}


def run_cfa_out(frame_c: Path = FRAME_C, draws: int = 2000) -> dict:
    """C11: C05's reading without pegs, the CFA unions' members left out."""
    rows = counted(read_csv(frame_c / "series.csv"))
    members = cfa_members()
    kept = [r for r in rows if r["money"] not in members]
    left = sorted({r["money"] for r in rows if r["money"] in members})
    return {"lines": len(kept), "left_out_lines": len(rows) - len(kept), "left_out_monies": left,
            "supports_count_without_pegs": reading(kept, "supports_count_without_pegs", draws)}


# --- C13: the institution line read by M0's text ----------------------------------------------------------------
#
# M0 section 2: *a limit by institution* stands on Garriga's index at or above 0.5, or a target announced. Frame c
# coded the second arm "cannot be read until M4" (M3-panel c6) and so never read the line "no". C13 reads both arms:
# the targets from frame a (Hammond's 27 at the start of 2012 with their dates, the three exits, the AREAER
# candidates from 2012), and "no" where the index is read below the line and no target is announced.

AREAER_FIRST = re.compile(r"first listed in the AREAER (\d{4})")
#: Frame a's pre-2012 adopters that Hammond's 27 do not hold (gap G08; its MANIFEST, members): Paraguay by the
#: resolution of 18 May 2011 the BCP recounts; Uganda by its July 2011 statement, which names a target already set, so
#: adopted by 2011 at a date unread. Uruguay's AREAER listing is a re-entry, its earlier target undated: cannot be read
#: in every year.
PRE_2012 = {"PRY": ("adopted", 2011), "UGA": ("adopted by", 2011), "URY": ("unread", None)}
AREAER_IT = ROOT / "data" / "reconstructed" / "ft001-a-areaer" / "it-column.csv"


def targets(frame_a: Path = FRAME_A) -> dict[str, tuple[str, int | None]]:
    """Frame a's inflation targets, per money: ("adopted", year), ("no", None), ("unread", None) or
    ("unread from", the AREAER edition that first lists it)."""
    adopted = {r["money"]: int(r["period"][:4]) for r in read_csv(frame_a / "series.csv") if r["route"] == "a4"}
    out: dict[str, tuple[str, int | None]] = {}
    for r in read_csv(frame_a / "members.csv"):
        if not r["panel"] in ("4", "4-from-2012"):
            continue
        m, member = r["code"], r["member"]
        if member == "yes":
            out[m] = ("adopted", adopted[m])
        elif member == "no":
            out[m] = ("no", None)
        elif r["panel"] == "4":
            out[m] = ("unread", None)          # Hammond's exits, each on adopting the euro: dates not read
        else:
            out[m] = ("unread from", int(AREAER_FIRST.search(r["reason"]).group(1)))   # G06
    out = {**out, **PRE_2012}
    # R-A3: a money in the AREAER 2011 edition's inflation-targeting column is a targeter already; one on no other
    # list (the narrow check's m3: Albania, Georgia, Moldova) targeted by 2011, at a date frame a does not read.
    for r in read_csv(AREAER_IT):
        if r["edition"] == "2011" and r["money"] not in out:
            out[r["money"]] = ("adopted by", 2011)
    return out


def target_at(money: str, year: int, t: dict[str, tuple[str, int | None]]) -> str:
    """'yes' if a target was announced before the entry year, 'no' if none was, else 'cannot be read'. A money on
    neither list is no targeter: Hammond's 27 and three exits to 2012, with the pre-2012 adopters frame a found beyond
    them (G08; and the AREAER 2011 column's, R-A3) and Uruguay's earlier target unread; the AREAER's column every
    candidate after. "Adopted by" a year: a target before it at a date unread, so "yes" only after it. An adoption in
    the entry year itself cannot be ordered against the entry: cannot be read."""
    kind, y = t.get(money, ("no", None))
    if kind == "adopted":
        return "yes" if y < year else ("cannot be read" if y == year else "no")
    if kind == "unread from":
        return "no" if year < y else "cannot be read"
    if kind == "adopted by":
        return "yes" if year > y else "cannot be read"
    return "no" if kind == "no" else "cannot be read"


def institution_m0(index: float | None, target: str, line: float = 0.5) -> str:
    if (index is not None and index >= line) or target == "yes":
        return "yes"
    if index is not None and target == "no":
        return "no"
    return "cannot be read"


def count(items: list[str]) -> str:
    """panel.supports' count, unchanged."""
    yes = sum(v == "yes" for v in items)
    unknown = sum(v == "cannot be read" for v in items)
    if yes >= 2:
        return TWO
    if yes + unknown <= 1:
        return FEWER
    return "cannot be read"


class Inputs:
    """Frame c's inputs to panel.supports, read as strain.py reads them."""

    def __init__(self):
        import panel as P
        self.P, self.garriga, self.ka, self.irr = P, P.garriga(), P.ka_open(), P.irr_classes()
        self.targets = targets()

    def supports(self, row: dict, m0: bool, cap_line: float = 0.5, index_line: float = 0.5,
                 ka_line: float = 0.25) -> dict[str, str]:
        m, year = row["money"], int(str(row["entry_date"])[:4])
        gv = self.garriga.get(m, {}).get(year, {})
        cls, _ = self.P.class_at(self.irr.get(m), year)
        sup = self.P.supports(row["default_at_entry"], gv.get("cuk_limlen"), cls, gv.get("lvau_garriga"),
                              self.ka.get(m, {}).get(year), cap_line=cap_line, index_line=index_line, ka_line=ka_line)
        if not m0:
            return sup
        inst = institution_m0(gv.get("lvau_garriga"), target_at(m, year, self.targets), index_line)
        tb, rule, cap, force = sup["taken_back"], sup["limit_by_rule"], sup["limit_by_rule_cap_only"], sup["force"]
        return {**sup, "limit_by_institution": inst, "supports_count": count([tb, rule, inst, force]),
                "supports_count_without_pegs": count([tb, cap, inst, force]),
                "supports_count_without_taken_back": count([rule, inst, force])}


GRID = {"supports_count_cap_025": {"cap_line": 0.25}, "supports_count_cap_075": {"cap_line": 0.75},
        "supports_count_index_04": {"index_line": 0.4}, "supports_count_index_06": {"index_line": 0.6},
        "supports_count_ka_01": {"ka_line": 0.1}, "supports_count_ka_05": {"ka_line": 0.5}}
COLUMNS = SUPPORTS + ("limit_by_rule_cap_only",) + READINGS


def reread(rows: list[dict], inp: Inputs, m0: bool = True) -> list[dict]:
    """Each line with its supports and counts recomputed (m0: the institution line by M0's text)."""
    out = []
    for r in rows:
        sup = inp.supports(r, m0)
        new = {**r, **{k: sup[k] for k in COLUMNS}}
        for k, kw in GRID.items():
            new[k] = inp.supports(r, m0, **kw)["supports_count"]
        out.append(new)
    return out


def reproduces(rows: list[dict], inp: Inputs) -> list[str]:
    """The self-check before any reading: recomputed without M0's second arm, every line's columns equal frame c's."""
    bad = []
    for r, n in zip(rows, reread(rows, inp, m0=False)):
        bad += [f"{r['money']} {r['entry_date']} {k}: {r[k]} != {n[k]}" for k in COLUMNS + tuple(GRID) if r[k] != n[k]]
    return bad


def run_m0(frame_c: Path = FRAME_C, draws: int = 2000) -> dict:
    """C13: C05's run and C11's reading with the institution line read by M0's text."""
    inp = Inputs()
    head = counted(read_csv(frame_c / "series.csv"))
    bad = reproduces(head, inp)
    if bad:
        raise ValueError(f"frame c's supports not reproduced ({len(bad)}): {bad[:5]}")
    rows = reread(head, inp)
    out: dict = {"lines": len(rows), "monies": len({r["money"] for r in rows})}
    out["institution_lines"] = {v: sum(r["limit_by_institution"] == v for r in rows)
                                for v in ("yes", "no", "cannot be read")}
    out["institution_lines_frame_c"] = {v: sum(r["limit_by_institution"] == v for r in head)
                                        for v in ("yes", "no", "cannot be read")}
    out["readings"] = {k: reading(rows, k, draws) for k in READINGS}
    out["claim"] = claim_verdict(*(out["readings"][k]["outcome"] for k in READINGS))
    out["each_support_alone"] = {k: reading(rows, k, draws) for k in SUPPORTS}
    no_war = [r for r in rows if not war_in_h(r)]
    out["war_in_H_out"] = {"lines": len(no_war), **{k: reading(no_war, k, draws) for k in READINGS}}
    out["frame_c_variants"] = {}
    for name in VARIANT_FILES:
        vrows = counted(read_csv(frame_c / f"variant-{name}.csv"))
        bad = reproduces(vrows, inp)
        vrows = reread(vrows, inp)
        out["frame_c_variants"][name] = {"lines": len(vrows), "not_reproduced": len(bad),
                                         **{k: reading(vrows, k, draws) for k in READINGS}}
    out["separator_variants"] = {k: reading(rows, k, draws) for k in SEPARATOR_VARIANTS}
    for k in READINGS:
        same = [v[k]["outcome"] == out["readings"][k]["outcome"] for v in
                list(out["frame_c_variants"].values()) + [out["war_in_H_out"]]]
        out.setdefault("variants_counted", {})[k] = f"{sum(same)} of {len(same)} variants tell the same outcome"
    members = cfa_members()
    kept = [r for r in rows if r["money"] not in members]
    out["cfa_out"] = {"lines": len(kept), "left_out_lines": len(rows) - len(kept),
                      "supports_count_without_pegs": reading(kept, "supports_count_without_pegs", draws)}
    return out


def composition(rows: list[dict], key: str) -> dict[str, list[int]]:
    """The spells in strata with both sides, by default at entry: {default: [n one or none, n two or more]}."""
    out: dict[str, list[int]] = {"yes": [0, 0], "no": [0, 0]}
    for s, (s0, s1) in strata(rows, key).items():
        if s0 and s1:
            out[s[-1]][0] += len(s0)
            out[s[-1]][1] += len(s1)
    return out


def m0_lines(frame_c: Path = FRAME_C) -> list[dict]:
    """C13's headline lines, re-read (for the registry's descriptions of them)."""
    inp = Inputs()
    head = counted(read_csv(frame_c / "series.csv"))
    if reproduces(head, inp):
        raise ValueError("frame c's supports not reproduced")
    return reread(head, inp)


def main(card: Path = CARD) -> Path:
    """Runs C05 (the default) or, given C11's or C13's path, that card."""
    from ft import cards
    cards.require_locked(card)
    result = run() if card == CARD else run_cfa_out() if card == CARD_CFA else run_m0()
    return cards.write_result(STUDY, card, result)


if __name__ == "__main__":
    print(main())
