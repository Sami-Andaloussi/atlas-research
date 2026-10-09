"""The readings (BLUEPRINT §5 d; P01, P03): what each claim's estimate means, written into the registry beside
its value, and the labels every printed number carries (measure, period, population; W4).

Run after ``registry.py`` (``run.py`` calls it): it reads ``results/numbers.json``, adds the fields and saves.
It changes no value and reruns no card: the estimates are the cards' runs and the committed builds, as
registered. It adds a few numbers, each computed here from what is already frozen or registered (``extras``).

**The size that matters** of these claims was set on 2026-10-07, in the regeneration under the revised engine
(the E1 session for arc E2), **after the results were seen**: the cards predate the field (``matters``),
except claim 2's margin of ten points, which its card fixed before the run. Each size is set from what a reader
would act on or retell, never from the result, by the rule part 2 used: **one point**, of a note's value or of
inflation a year, is the smallest change a holder notices and would retell; claim 2's ten points are its
card's; a ratio of the chance of a crisis is read against half as likely again (1.5), the smallest a reader
would retell as "more likely". The record is ``check/2026-10-06-readings.md``; the isolated checker judges each
line.

The readings are judgements (P01): ``effect``, ``too small to matter`` or ``bounded`` (W18, round 2: the legacy
"could not tell" is read by the engine's P03 where the key has a range, and dropped where it has none). Code
(``ft.readiness``) refuses only a reading its own range contradicts.
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STUDY = HERE.parent
ROOT = STUDY.parents[1]
REC = ROOT / "data" / "reconstructed"
sys.path.insert(0, str(HERE))

from ft import numbers  # noqa: E402

M_PTS, M_RATIO = 1.0, 1.5
#: claim 2's smallest difference that counts, fixed on its card before the run (M0 section 6)
M_HELD = "c2_margin"

#: the Tooke dates read for the notes' value in the first years of the suspension (the A3 build's cross-check)
PAR_FROM, PAR_TO = "1797-08", "1799-08"

#: key -> (claim type, the low key, the high key, matters, null, reading); a range given by its two keys.
CLAIMS: dict[str, tuple] = {
    # the door, 1797-1799: the notes' value in gold at Tooke's dates, the headline (added by extras)
    "door_par_value": ("descriptive", "door_par_low", "door_par_high", M_PTS, 0, "too small to matter"),
    # a support changed (the window build, A2): a mean gap against matched monies with a band drawn under no
    # effect, and no interval for the gap itself; the bands run several points either side, so a gap of one
    # point could not be told from none (A3 of the register)
    "a2_p1_mean": ("comparative", None, None, M_PTS, 0, "could not tell"),
    "a2_p2_mean": ("comparative", None, None, M_PTS, 0, "could not tell"),
    "a2_p3d_mean": ("comparative", None, None, M_PTS, 0, "could not tell"),
    "a2_p3u_mean": ("comparative", None, None, M_PTS, 0, "could not tell"),
    "a2_p4_mean": ("comparative", None, None, M_PTS, 0, "could not tell"),
    "a2_p4v_mean": ("comparative", None, None, M_PTS, 0, "could not tell"),
    # who held under the same stress (claim 2, C13; C05 and C11 on the first coding)
    "c2_head_d": ("comparative", "c2_head_lo", "c2_head_hi", M_HELD, 0, "could not tell"),
    "c2_tb_d": ("comparative", "c2_tb_lo", "c2_tb_hi", M_HELD, 0, "could not tell"),
    "c2_np_d": ("comparative", "c2_np_lo", "c2_np_hi", M_HELD, 0, "could not tell"),
    "c2_np_d_nocfa": ("comparative", "c2_np_lo_nocfa", "c2_np_hi_nocfa", M_HELD, 0, "could not tell"),
    "c2_c05_head_d": ("comparative", None, None, M_HELD, 0, "could not tell"),
    "c2_c05_np_d": ("comparative", None, None, M_HELD, 0, "could not tell"),
    "c2_c11_d": ("comparative", None, None, M_HELD, 0, "could not tell"),
    # claim 1, counted forward within the pressure strata: one year on each side
    "c1_fwd_b_ratio": ("comparative", None, None, M_RATIO, 1, "could not tell"),
}

#: The measurements a reader sees without a claim on them: their type only. Claim 1 is a description by
#: design (its card: five rounds found strain before both the act and the crisis); A3 is a model's reading
#: with no verdict; frame k is told, not counted; the coins and today's table are coded lines.
DESCRIPTIVE = (
    "c1_after_sr", "c1_base_sr", "c1_tot_after_sr", "c1_tot_base_sr", "c1_prv_after_sr", "c1_prv_base_sr",
    "c1_same_sr", "c1_before_sr", "c1_none_sr", "c1_tot_same_sr", "c1_tot_before_sr", "c1_tot_none_sr",
    "a3_restriction_wait_low", "a3_restriction_wait_high", "a3_greenback_wait_low", "a3_greenback_wait_high",
    "a3_restriction_p_low", "a3_greenback_p_low", "a3_restriction_premium_low",
    "c4_coins_none", "c4_coins", "c4_coins_none_pct", "c4_redeem_any", "c4_redeem_account", "c4_kappa",
    "now_usd_index", "now_usd_cofer", "now_eur_cofer", "c3_open_n", "c3_closed_n",
)


def labels() -> dict[str, tuple[str, str, str]]:
    """key -> (measure, period, population), for every key a reader's text prints (filled in ``LABELS``)."""
    try:
        from labels import LABELS  # noqa: PLC0415  (the printed keys' labels, written with the forms)
    except ImportError:
        return {}
    return LABELS


def extras(entries: dict) -> None:
    """The numbers the regenerated forms add, each computed here from what is frozen or registered: the sizes
    that matter, and the notes' value in gold at Tooke's dates from August 1797 to August 1799 (the A3 build's
    cross-check of Tooke's semiannual table, ``variant-cross-source.csv``: the notes' value in gold, par = 1)."""
    for key, value, unit, fmt in (("matters_pts", M_PTS, "points", "{:.0f}"),
                                  ("matters_ratio", M_RATIO, "times as likely", "{:.1f}")):
        entries[key] = {"value": value, "unit": unit, "fmt": fmt, "as_of": "2026-10-07",
                        "origin": {"kind": "computed", "script": "code/readings.py"},
                        "note": "a size that matters, set on 2026-10-07 after the results were seen "
                                "(check/2026-10-06-readings.md)"}
    with open(REC / "ft001-a3" / "variant-cross-source.csv", newline="", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if r["case"] == "the Bank Restriction" and r["P"]
                and PAR_FROM <= r["period"] <= PAR_TO]
    v = [100 * (float(r["P"]) - 1) for r in rows]
    origin = {"kind": "computed", "script": "code/readings.py (the A3 build, its cross-check of Tooke's table)"}
    common = {"as_of": entries["as_of"]["value"], "origin": origin}
    entries["door_par_dates"] = {"value": len(v), "unit": "dates", **common}
    entries["door_par_value"] = {"value": sum(v) / len(v), "unit": "percent of the notes' gold value, above par",
                                 "fmt": "{:+.1f}%", **common,
                                 "note": "the mean over Tooke's dates; low and high are the lowest and highest "
                                         "date, not a sampling interval: the case is one money"}
    entries["door_par_low"] = {"value": min(v), "unit": "percent of the notes' gold value, above par",
                               "fmt": "{:+.1f}%", **common}
    entries["door_par_high"] = {"value": max(v), "unit": "percent of the notes' gold value, above par",
                                "fmt": "{:+.1f}%", **common}


def engine_reading(e: dict) -> str:
    """The engine's P03 (``ft.readiness.reading_problems``; the engine's ruling of 2026-10-08): too small to matter if
    the range lies inside null +- m; an effect if it excludes the null and is not wholly inside; bounded otherwise."""
    null, m, lo, hi = e.get("null", 0) or 0, abs(e["matters"]), e["low"], e["high"]
    if null - m <= lo and hi <= null + m:
        return "too small to matter"
    if lo > null or hi < null:
        return "effect"
    return "bounded"


def apply(path: Path | None = None) -> None:
    path = path or STUDY / "results" / "numbers.json"
    body = json.loads(path.read_text())
    entries = body["numbers"]
    extras(entries)
    for key, (ctype, lo, hi, matters, null, reading) in CLAIMS.items():
        e = entries[key]
        e["claim_type"] = ctype
        if lo:
            e["low"], e["high"] = float(entries[lo]["value"]), float(entries[hi]["value"])
        e["matters"] = float(entries[matters]["value"]) if isinstance(matters, str) else matters
        if null:
            e["null"] = null
        if reading == "could not tell":  # W18 (round 2): the legacy word is never written
            reading = engine_reading(e) if lo else None
            null, m = e.get("null", 0) or 0, abs(e["matters"])
            if reading == "effect" and not (e["low"] > null + m or e["high"] < null - m):
                e["note"] = (f"the range excludes {null:g} but its near end lies short of the size that matters "
                             f"({m:g}): it rules out no difference, not one smaller than {m:g} (the engine's ruling "
                             "of 2026-10-08)")
        if reading is None:
            e.pop("reading", None)  # a reading is what a range rules out: a key with no range carries none
        else:
            e["reading"] = reading
    for key in DESCRIPTIVE:
        entries[key].setdefault("claim_type", "descriptive")
    for e in entries.values():  # a rule's parameter, cited from the study's rules: their name goes to the locator
        o = e.get("origin") or {}
        if o.get("kind") == "cited" and str(o.get("source", "")).startswith(("M0 ", "A3 card")):
            o["locator"] = "; ".join(x for x in (o["source"], o.get("locator")) if x)
            o["source"] = "First Thing: a rule fixed before the analysis ran (see the methods and proof)"
    for key, (measure, period, population) in labels().items():
        entries[key].update(measure=measure, period=period, population=population)
    for key, e in entries.items():
        numbers.Registry._validate_reading(key, e)  # the new fields' shape, and low <= value <= high
    path.write_text(json.dumps(body, indent=2, ensure_ascii=False) + "\n")
    numbers.Registry.load(path)


if __name__ == "__main__":
    apply()
