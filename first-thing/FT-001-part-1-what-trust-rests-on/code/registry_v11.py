"""The numbers of map v11's new cards (round 2, 2026-10-08): CS-D (C16), CS-A (C18), CS-B (C19) and its correction
(C20), written into the registry beside the reused numbers (``registry.py`` calls :func:`add`). C17 is void (its card's
item 7) and registers no number.

Each estimate sits under its card's matters key (the engine reads a key's size that matters from its card by name),
with its labels, range, size that matters and the engine's reading (P03 as ``ft.readiness`` holds it; the engine's
ruling of 2026-10-08). Where the card's stricter wording (an effect only if the whole range lies beyond the size that
matters) reads otherwise, the note says so. A ratio's size that matters (C16's 1.5 times) is a factor: its keys carry
``scale: ratio`` (the engine's d2b39410), the band 1/1.5 to 1.5 around a null of 1. Nothing is recomputed: each value is the card's run as committed.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
STUDY = HERE.parent
RUNS = STUDY / "results" / "runs"
sys.path.insert(0, str(HERE))

PTS = "points of inflation a year"
F2, F1 = "{:.2f}", "{:.1f}"


def run(card: str) -> dict:
    return json.loads((RUNS / f"{card}.json").read_text())["result"]


def matters(card: str) -> dict:
    return yaml.safe_load((STUDY / "cards" / f"{card}.yaml").read_text())["matters"]


def card_reading(lo: float, hi: float, m: float, null: float = 0.0) -> str:
    if lo > null + m or hi < null - m:
        return "effect"
    if null - m <= lo and hi <= null + m:
        return "too small to matter"
    return "bounded"


def reading(lo: float, hi: float, m: float, null: float = 0.0) -> str:
    if null - m <= lo and hi <= null + m:
        return "too small to matter"
    if lo > null or hi < null:
        return "effect"
    return "bounded"


def est(R, mkey: str, prefix: str, value: float, lo: float, hi: float, m: float, s: str, labels: dict,
        unit: str = PTS, claim_type: str = "comparative", note: str = "") -> None:
    rd, cr = reading(lo, hi, m), card_reading(lo, hi, m)
    if rd != cr:
        note = "; ".join(x for x in (note, f"the card's own rule (an effect only if the whole range lies beyond "
                                     f"{m:g}) reads it {cr}: the range excludes 0 but its near end lies short of "
                                     f"{m:g}") if x)
    R.reg.put(mkey, value, unit=unit, origin={"kind": "computed", "script": s}, as_of=R.AS_OF, fmt=F1, low=lo,
              high=hi, null=0.0, matters=m, reading=rd, claim_type=claim_type, note=note, **labels)
    R.put(f"{prefix}_lo", lo, unit, s, fmt=F1)
    R.put(f"{prefix}_hi", hi, unit, s, fmt=F1)


def cs_a(R) -> None:
    out, s, mt = run("C18-cs-a-consumer-prices-off-gold"), "code/cs_a.py (card C18)", \
        matters("C18-cs-a-consumer-prices-off-gold")
    pop = "15 rich economies"
    for key, mk, name in (("main", "cs_a_pooled", "csa"), ("no_exchange_control", "cs_a_pooled_no_exchange_control",
                                                           "csa_noxc"), ("no_spain", "cs_a_pooled_no_spain",
                                                                         "csa_noesp")):
        b = out[key]
        assert reading(b["lo"], b["hi"], mt[mk]) == "bounded" == b["reading"]
        est(R, mk, name, b["pooled"], b["lo"], b["hi"], mt[mk], s,
            {"measure": "consumer-price inflation off gold less on gold", "period": "1932-34", "population": pop})
        R.put(f"{name}_half", b["half_width"], PTS, s, fmt=F1)
        R.put(f"{name}_half_doubled", b["doubled"]["half_width"], PTS, s, fmt=F1)
    for y, v in out["main"]["by_year"].items():
        R.put(f"csa_year_{y}", v, PTS, s, fmt=F1)
    R.put("csa_economies", len(out["economies"]), "economies", s)


def cs_b(R) -> None:
    s19, s20 = "code/cs_b.py (card C19)", "code/cs_b_trim.py (card C20)"
    r19, m19 = run("C19-cs-b-inflation-by-convertibility"), matters("C19-cs-b-inflation-by-convertibility")
    r20, m20 = run("C20-cs-b-without-hyperinflation-years"), matters("C20-cs-b-without-hyperinflation-years")
    assert not r20["void"]
    pop = "17 rich economies"
    lab = {"measure": "mean gap, inconvertible less convertible", "period": "1870-2020 minus wars and Bretton Woods",
           "population": pop}
    carried = ("carried by Germany's 1920-24 years above 100% a year; C20 corrects it with those years set apart")
    for key, mk in (("main", "cs_b_gap"), ("fiat_from_1972", "cs_b_gap_from_1972"),
                    ("no_transition_years", "cs_b_gap_no_transition"),
                    ("own_block_returns_only", "cs_b_gap_own_block_returns"),
                    ("earlier_resumption", "cs_b_gap_earlier_resumption"),
                    ("marked_suspensions_inconvertible", "cs_b_gap_marked_suspensions")):
        b = r19[key]
        est(R, mk, f"c19_{key}", b["gap"], b["interval"][0], b["interval"][1], m19[mk], s19, lab,
            note="" if key == "fiat_from_1972" else carried)
    for key, mk in (("main", "cs_b_gap_set_apart"), ("fiat_from_1972", "cs_b_gap_set_apart_from_1972"),
                    ("log_rates", "cs_b_log_gap"), ("log_rates_set_apart", "cs_b_log_gap_set_apart"),
                    ("no_transition_years", "cs_b_gap_set_apart_no_transition"),
                    ("own_block_returns_only", "cs_b_gap_set_apart_own_block_returns"),
                    ("earlier_resumption", "cs_b_gap_set_apart_earlier_resumption"),
                    ("marked_suspensions_inconvertible", "cs_b_gap_set_apart_marked_suspensions")):
        b = r20[key]
        est(R, mk, f"c20_{key}", b["gap"], b["interval"][0], b["interval"][1], m20[mk], s20,
            {**lab, "measure": "mean gap in log inflation, inconvertible less convertible"} if "log" in key else
            {**lab, "period": "1870-2020 minus wars, Bretton Woods, 100%+ years"})
    mg = r20["median_gap"]
    est(R, "cs_b_median_gap", "c20_median", mg["gap"], mg["interval"][0], mg["interval"][1], m20["cs_b_median_gap"],
        s20, {**lab, "measure": "median gap, inconvertible less convertible"})
    R.put("c19_economies", len(r19["economies"]), "economies", s19)
    R.put("c20_float_years_above_line", r20["fiat_from_1972_years_above"], "economy-years above 100% a year", s20)
    for c, v in r20["by_class"].items():
        R.put(f"c20_{c}_share10", 100 * v["share_above_10"], "percent of economy-years above 10% a year", s20,
              fmt="{:.0f}%")
        R.put(f"c20_{c}_n", v["n"], "economy-years", s20)
        R.put(f"c20_{c}_mean", v["mean"], "percent a year", s20, fmt="{:.1f}%")
        R.put(f"c20_{c}_median", v["median"], "percent a year", s20, fmt=F1)
    R.put("c20_set_apart", len(r20["set_apart"]), "economy-years", s20)
    for era, x in r20["eras"].items():
        for c in ("convertible", "fiat"):
            if x[c]["n"]:
                R.put(f"c20_era_{era.replace('-', '_')}_{c}", x[c]["mean"], "percent a year", s20, fmt="{:.1f}%")
    # inconvertible years since 1972 by each economy's inflation-target adoption (C19 item 4; reported since the
    # grid check of 2026-10-08, 2-6): no year above 100% in any group, so C19's means stand as they are
    for g, name in (("before_adoption", "before"), ("from_adoption", "from"), ("no_counted_adoption", "none")):
        x = r19["fiat_from_1972_by_target"][g]
        assert x["above_100"] == 0, g
        R.put(f"c19_target_{name}_mean", x["mean"], "percent a year", s19, fmt="{:.1f}%")
        R.put(f"c19_target_{name}_n", x["n"], "economy-years", s19)
    # the same years, matched (the confirming check of 2026-10-08): every counted adoption came in 1991 or later, so
    # the economies with no adoption are averaged over the adopters' own target years, from C19's frozen panel
    import cs_b as B
    import numpy as np
    d, _ = B.panel(yaml.safe_load(B.CARD.read_text())["parameters"])
    adopt = B.adoption_years()
    f72 = d[(d["class"] == "fiat") & (d.year >= 1972)]
    from_ = f72[f72.apply(lambda r: r.iso in adopt and r.year >= adopt[r.iso], axis=1)]
    none = f72[~f72.iso.isin(adopt)]
    assert abs(from_.pi.mean() - r19["fiat_from_1972_by_target"]["from_adoption"]["mean"]) < 1e-9
    assert int(from_.year.min()) == 1991, from_.year.min()
    by_year = none.groupby("year").pi.mean()
    matched = float(np.mean([by_year[y] for y in from_.year]))
    R.put("c19_target_none_matched", matched, "percent a year", "code/registry_v11.py from C19's panel (code/cs_b.py)",
          fmt="{:.1f}%")
    for c in ("convertible", "fiat"):
        R.put(f"c19_{c}_n", r19["by_class"][c]["n"], "economy-years", s19)
        R.put(f"c19_{c}_median", r19["by_class"][c]["median"], "percent a year", s19, fmt=F1)


def cs_d(R) -> None:
    out, s = run("C16-cs-d-default-ratio"), "code/cs_d.py (card C16)"
    assert not out["void"]
    mt = matters("C16-cs-d-default-ratio")
    keys = {"headline": "cs_d_ratio", "without_T2": "cs_d_ratio_without_t2", "T2-var-total": "cs_d_ratio_t2_total",
            "T2-var-private": "cs_d_ratio_t2_private", "shared_once": "cs_d_ratio_shared_once"}
    for name, mk in keys.items():
        r = out["readings"][name]
        p = f"csd_{name.lower().replace('-', '_')}"
        for k in ("after", "readable", "with_act", "readable_trials"):
            R.put(f"{p}_{k}", r[k], "events" if k in ("after", "readable") else "strained years", s)
        if r["degenerate"]:
            continue  # 0 or 1 break after an act: counts printed, no ratio read (the card's item 5)
        i = r["interval"]
        m = mt[mk]
        if i["lo"] >= 1 / m and i["hi"] <= m:
            rd = "too small to matter"
        elif i["lo"] > 1 or i["hi"] < 1:
            rd = "effect"
        else:
            rd = "bounded"
        note = "" if rd == i["reading"] else f"the card's own rule reads the range {i['reading']}"
        R.reg.put(mk, r["ratio"], unit="times", origin={"kind": "computed", "script": s}, as_of=R.AS_OF, fmt=F2,
                  low=i["lo"], high=i["hi"], matters=m, scale="ratio", reading=rd, claim_type="comparative",
                  note=note,
                  measure="share of readable money crises after an act over share of readable strained years with "
                          "one", period="1970 to the panel's common end",
                  population="C07's R10 population: breaks and strained years from the same spells")
        R.put(f"{p}_lo", i["lo"], "times", s, fmt=F2)
        R.put(f"{p}_hi", i["hi"], "times", s, fmt=F2)
        y = r["by_onset_year"]
        R.put(f"{p}_year_lo", y["lo"], "times", s, fmt=F2)
        R.put(f"{p}_year_hi", y["hi"], "times", s, fmt=F2)
        R.put(f"{p}_clusters", i["clusters"], "clusters", s)


def add(R) -> None:
    R.AS_OF = "2026-09-30"  # JST R6's vintage; C16 reads C15's builds, frozen by then
    cs_a(R)
    cs_b(R)
    cs_d(R)
