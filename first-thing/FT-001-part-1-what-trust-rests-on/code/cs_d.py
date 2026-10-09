"""Card C16 (CS-D, C15's child): on C07's R10 population, the ratio of the share of money crises that came after a
headline act to the share of strained years that held with one, and its interval by money.

From the study's folder: ``../../toolkit/bin/ftpy code/cs_d.py``. Writes ``results/runs/C16-cs-d-default-ratio.json``.

Readings of the card that its text leaves to the code, fixed here before the run:

- *The rebuild*: ``claim1.run_v3``'s inputs and ``build_result_v2``'s steps up to the breaks, trials, acts, coverage and
  R10 population, with claim1's own functions; nothing re-implemented but the per-unit marks, which call claim1's
  ``break_classes`` and ``base_rate_year`` as ``shares`` and ``base_rate`` do.
- *Readable*: a break not "cannot be read" (C15's share_of_readable); a trial marked "act" or "no act".
- *Shared once* (R8): ``claim1.shared_once`` on the breaks, then R10 kept.
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import claim1 as C  # noqa: E402

from ft import cards  # noqa: E402

CARD = C.STUDY / "cards" / "C16-cs-d-default-ratio.yaml"
GROUPS = {  # the card's item 4: the members of one money share one cluster
    "CFA franc": ["BEN", "BFA", "CIV", "GNB", "MLI", "NER", "SEN", "TGO", "CMR", "CAF", "TCD", "COG", "GNQ", "GAB"],
    "East Caribbean dollar": ["ATG", "DMA", "GRD", "KNA", "LCA", "VCT"],
    "rand area": ["LSO", "SWZ"],
    "US dollar users": ["ECU", "PAN", "FSM", "MHL", "PLW"],
    "euro users outside the area": ["MNE", "SMR"],
}
CLUSTER = {m: g for g, ms in GROUPS.items() for m in ms}
C15_RUN = C.STUDY / "results" / "runs" / "C15-claim1-institution-m0.json"


def rebuild(data: Path = C.DATA) -> dict:
    reader = C.PanelReader()
    frame_c = C.m0_frame_c(C.read_csv(data / "ft001-c" / "series.csv"))
    frame_b = C.read_csv(data / "ft001-b" / "series.csv")
    acts_rows = C.read_csv(data / "ft001-acts" / "series.csv")
    coverage = C.build_coverage(C.read_csv(data / "ft001-acts" / "coverage.csv"))
    spells, left = C.prepare_spells(frame_c)
    all_counted = left.pop("all_counted")
    by_money: dict[str, list[dict]] = defaultdict(list)
    for s in all_counted:
        by_money[s["money"]].append(s)
    breaks = C.prepare_breaks(frame_b, set(by_money))
    trials, _ = C.build_trials(spells, reader, reader.end)
    population = {(s["money"], s["onset_year"]) for s in spells if s["onset_year"] is not None}
    acts = {"headline": C.headline_acts(acts_rows),
            "T2-var-total": C.headline_acts(acts_rows, "T2-var-total"),
            "T2-var-private": C.headline_acts(acts_rows, "T2-var-private")}
    return {"breaks": breaks, "trials": trials, "population": population, "acts": acts, "coverage": coverage}


def r10(b: dict, breaks: list[dict]) -> list[dict]:
    return [x for x in breaks if (x["money"], x["onset_year"]) in b["population"]]


def units(b: dict, reading: str, codes: tuple, keep_act, pop: list[dict]) -> tuple[list[tuple], list[tuple]]:
    """(money, year, class) for each R10 break and (money, year, mark) for each trial, under one reading."""
    acts, coverage = b["acts"][reading], b["coverage"]
    classes = C.break_classes(pop, acts, lambda m: (coverage.get(m, {}).get("by_code", {}), codes), keep_act)
    marks = []
    for t in b["trials"]:
        cov = coverage.get(t["money"], {}).get("by_code", {})
        marks.append((t["money"], t["y"], C.base_rate_year(t["y"], C.act_filter(acts, t["money"], codes),
                                                   C.window_readable(cov, codes, t["y"] - C.L, t["y"] - 1))))
    return [(x["money"], x["onset_year"], c) for x, c in zip(pop, classes)], marks


def counts(br: list[tuple], tr: list[tuple]) -> dict:
    cls = [u[-1] for u in br]
    after = sum(c == C.AFTER for c in cls)
    readable = sum(c != C.UNREAD for c in cls)
    act = sum(u[-1] == "act" for u in tr)
    no_act = sum(u[-1] == C.NO_ACT for u in tr)
    out = {"breaks": len(br), "after": after, "readable": readable, "trials": len(tr), "with_act": act,
           "readable_trials": act + no_act, "no_act_trials": no_act, "unread_trials": len(tr) - act - no_act,
           "classes": {k: cls.count(k) for k in (C.AFTER, C.SAME, C.BEFORE, C.NO_ACT, C.UNREAD)}}
    s1 = after / readable if readable else None
    s0 = act / (act + no_act) if act + no_act else None
    out.update({"share_breaks": s1, "share_trials": s0, "ratio": (s1 / s0) if s1 is not None and s0 else None})
    return out


def reading(lo: float, hi: float, line: float) -> str:
    if lo > line:
        return "effect"
    if hi < 1 / line:
        return "effect of the other sign"
    if lo >= 1 / line and hi <= line:
        return "too small to matter"
    return "bounded"


def bootstrap(br: list[tuple], tr: list[tuple], draws: int, seed: int, line: float, key) -> dict:
    by = defaultdict(lambda: ([], []))
    for u in br:
        by[key(u)][0].append(u[-1])
    for u in tr:
        by[key(u)][1].append(u[-1])
    monies = sorted(by)
    rng = np.random.default_rng(seed)
    ratios, skipped = [], 0
    for _ in range(draws):
        pick = rng.choice(len(monies), size=len(monies), replace=True)
        b_, t_ = [], []
        for i in pick:
            cs, ks = by[monies[i]]
            b_ += [("", c) for c in cs]
            t_ += [("", k) for k in ks]
        r = counts(b_, t_)["ratio"]
        if r is None or counts(b_, t_)["readable"] == 0:
            skipped += 1
            continue
        ratios.append(r)
    lo, hi = (float(v) for v in np.percentile(ratios, [2.5, 97.5]))
    rd = reading(lo, hi, line)
    return {"lo": lo, "hi": hi, "draws_used": len(ratios), "skipped": skipped, "clusters": len(monies),
            "reading": rd, "refuted": rd != "bounded"}


def main() -> Path:
    card = yaml.safe_load(CARD.read_text())
    cards.require_locked(CARD)
    prm, mt = card["parameters"], card["matters"]
    stored = json.loads(C15_RUN.read_text())["result"]["readings"]
    b = rebuild()
    nT2 = tuple(c for c in C.HEADLINE if c != "T2")
    plan = {"headline": ("headline", C.HEADLINE, lambda a: True, b["breaks"], mt["cs_d_ratio"]),
            "without_T2": ("headline", nT2, lambda a: a["code"] != "T2", b["breaks"], mt["cs_d_ratio_without_t2"]),
            "T2-var-total": ("T2-var-total", C.HEADLINE, lambda a: True, b["breaks"], mt["cs_d_ratio_t2_total"]),
            "T2-var-private": ("T2-var-private", C.HEADLINE, lambda a: True, b["breaks"], mt["cs_d_ratio_t2_private"]),
            "shared_once": ("headline", C.HEADLINE, lambda a: True, None, mt["cs_d_ratio_shared_once"])}
    out, repro = {}, {}
    for name, (rd, codes, keep, brks, line) in plan.items():
        pop = C.shared_once(r10(b, b["breaks"])) if brks is None else r10(b, brks)
        br, tr = units(b, rd, codes, keep, pop)
        c = counts(br, tr)
        if name != "shared_once":
            key = "overall" if name != "without_T2" else "without_T2"
            s = stored["headline" if name in ("headline", "without_T2") else name]
            want_b, want_t = s["shares_base_rate_population"][key], s["base_rate"][key]
            stored_c = {"breaks": s["shares_base_rate_population"]["breaks"], "trials": want_t["years"],
                        "with_act": want_t["with_act"], "no_act_trials": want_t["no_act"],
                        "unread_trials": want_t["cannot_be_read"], "readable": want_b["readable"],
                        **{k: want_b[k]["n"] for k in (C.AFTER, C.SAME, C.BEFORE, C.NO_ACT, C.UNREAD)}}
            rebuilt_c = {"breaks": c["breaks"], "trials": c["trials"], "with_act": c["with_act"],
                         "no_act_trials": c["no_act_trials"], "unread_trials": c["unread_trials"],
                         "readable": c["readable"], **c["classes"]}
            repro[name] = {"stored": stored_c, "rebuilt": rebuilt_c, "reproduces": stored_c == rebuilt_c}
        degenerate = c["after"] <= 1
        out[name] = {**c, "degenerate": degenerate}
        if degenerate:
            out[name]["note"] = "0 or 1 break after an act: counts printed, no P03 reading (the card's item 5)"
        else:
            out[name]["interval"] = bootstrap(br, tr, prm["bootstrap_draws"], prm["seed"], line,
                                              lambda u: CLUSTER.get(u[0], u[0]))
            out[name]["by_onset_year"] = bootstrap(br, tr, prm["bootstrap_draws"], prm["seed"], line, lambda u: u[1])
    if not all(r["reproduces"] for r in repro.values()):
        return cards.write_result(C.STUDY, CARD, {"void": True, "why": "C15's stored counts not reproduced",
                                                  "reproduction": repro})
    payload = {"void": False, "reproduction": repro, "readings": out,
               "audits_beside": "1.26, 95% range 0.91-1.73 with a design effect of 6 (the map's audits, theirs)",
               "said": ["crises are events and strained years country-years",
                        "T2 is a creditor class newly in arrears, mostly inside a default already running (C15's t2)"],
               "t2_breadth": json.loads(C15_RUN.read_text())["result"]["t2"]}
    path = cards.write_result(C.STUDY, CARD, payload)
    print(path)
    return path


if __name__ == "__main__":
    main()
