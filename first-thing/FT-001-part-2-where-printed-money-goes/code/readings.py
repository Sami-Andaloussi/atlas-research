"""The readings (BLUEPRINT §5 d; P01, P03): what each claim's estimate means, written into the registry beside
its value, and the labels every printed number carries (measure, period, population; W4).

Run after ``registry.py`` (``run.py`` calls it): it reads ``results/numbers.json``, adds the fields and saves.
It changes no value and recomputes nothing: the estimates are the cards' runs, as registered.

**The size that matters** of these claims was set on 2026-10-06, in the regeneration under the revised
engine, **after the results were seen**: the cards predate the field (``matters``). Each size is set from what
a reader would act on or retell, never from the result, by one rule for every slope: the slope that moves
inflation by **one point a year** across the spread of its regressor that a reader meets. A point of
inflation a year is what changes a saver's choice. The spreads: ten points of money growth a year (what a
printing at the pace of the rich economies' purchases since 2008 adds, over a decade), so 0.1 for a slope on
money growth; four points of real output growth a year (a fast-growing economy against a slow one), so 0.25
for a slope on output growth. After a printing, a change of one point a year in inflation, or two points a
year in broad money growth (about a sixth of its median growth after a printing). Velocity's matters is the
card's own band (two standard deviations, C07 then C19), fixed before its run. The record is
``check/2026-10-06-readings.md``; the isolated checker judges each line.

The readings are judgements (P01): ``effect``, ``too small to matter`` or ``bounded`` (W18, round 2: a range that
holds the null and reaches past the size that matters, reported as what it rules out; it replaced the legacy word). Code
(``ft.readiness``) refuses only a reading its own range contradicts.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as K  # noqa: E402

from ft import numbers  # noqa: E402

M_SLOPE, M_GROWTH, M_PTS, M_BROAD, M_Z = 0.1, 0.25, 1.0, 2.0, 2.0

#: key -> (claim type, the low key, the high key, matters, null, reading); a range given by its two keys.
CLAIMS: dict[str, tuple] = {
    # the long run, 1950-2020, base money, the filled panel with the units guard (C28): the headline's three
    "lr_base_mu_below": ("comparative", "lr_base_mu_below_lo", "lr_base_mu_below_hi", M_SLOPE, 0, "effect"),
    "lr_base_mu_above": ("comparative", "lr_base_mu_above_lo", "lr_base_mu_above_hi", M_SLOPE, 0, "effect"),
    "lr_base_beta": ("descriptive", "lr_base_lo", "lr_base_hi", M_SLOPE, 0, "effect"),
    # beside the headline (context)
    "lr_base_gamma": ("descriptive", "lr_base_gamma_lo", "lr_base_gamma_hi", M_GROWTH, 0, "effect"),
    "lr_base_pi_below": ("comparative", "lr_base_pi_below_lo", "lr_base_pi_below_hi", M_SLOPE, 0, "effect"),
    "lr_base_pi_above": ("comparative", "lr_base_pi_above_lo", "lr_base_pi_above_hi", M_SLOPE, 0, "effect"),
    "lr_base_ho_beta": ("descriptive", "lr_base_ho_lo", "lr_base_ho_hi", M_SLOPE, 0, "effect"),
    "lr_c22_beta": ("descriptive", "lr_c22_lo", "lr_c22_hi", M_SLOPE, 0, "effect"),
    "lr_c22_ho_beta": ("descriptive", "lr_c22_ho_lo", "lr_c22_ho_hi", M_SLOPE, 0, "effect"),
    "lr_c22_mu_below": ("comparative", "lr_c22_mu_below_lo", "lr_c22_mu_below_hi", M_SLOPE, 0, "effect"),
    "lr_c22_mu_above": ("comparative", "lr_c22_mu_above_lo", "lr_c22_mu_above_hi", M_SLOPE, 0, "effect"),
    "lr_broad_beta": ("descriptive", "lr_broad_lo", "lr_broad_hi", M_SLOPE, 0, "effect"),
    "lr_broad_ho_beta": ("descriptive", "lr_broad_ho_lo", "lr_broad_ho_hi", M_SLOPE, 0, "effect"),
    "lr_broad_mu_below": ("comparative", "lr_broad_mu_below_lo", "lr_broad_mu_below_hi", M_SLOPE, 0, "effect"),
    "lr_broad_mu_above": ("comparative", "lr_broad_mu_above_lo", "lr_broad_mu_above_hi", M_SLOPE, 0, "effect"),
    "lr_base_2020_beta": ("descriptive", "lr_base_2020_lo", "lr_base_2020_hi", M_SLOPE, 0, "effect"),
    "lr_broad_2020_beta": ("descriptive", "lr_broad_2020_lo", "lr_broad_2020_hi", M_SLOPE, 0, "effect"),
    "lr_1870_beta": ("descriptive", "lr_1870_lo", "lr_1870_hi", M_SLOPE, 0, "effect"),
    "lr_1870_nowar_beta": ("descriptive", "lr_1870_nowar_lo", "lr_1870_nowar_hi", M_SLOPE, 0, "effect"),
    "lr_1870_gamma": ("descriptive", "lr_1870_gamma_lo", "lr_1870_gamma_hi", M_GROWTH, 0, "effect"),  # excludes 0, not inside the size that matters (W18)
    "lr_1870_mu_below": ("comparative", "lr_1870_mu_below_lo", "lr_1870_mu_below_hi", M_SLOPE, 0, "effect"),
    "lr_1870_mu_above": ("comparative", "lr_1870_mu_above_lo", "lr_1870_mu_above_hi", M_SLOPE, 0, "effect"),
    "lr_dgp_head_mu_below": ("comparative", "lr_dgp_head_mu_below_lo", "lr_dgp_head_mu_below_hi", M_SLOPE, 0, "effect"),  # excludes 0, not inside the size that matters (W18)
    "lr_dgp_head_mu_above": ("comparative", "lr_dgp_head_mu_above_lo", "lr_dgp_head_mu_above_hi", M_SLOPE, 0, "effect"),
    "lr_base_yield_beta": ("descriptive", "lr_base_yield_lo", "lr_base_yield_hi", M_SLOPE, 0, "effect"),
    # what decided, after a large printing (C26, the test of C18 on the filled prices): no range was computed
    # for a gap between two medians, only a permutation test; so no reading can say "too small to matter",
    # and none says "effect": each range holds 0 and reaches past the size that matters, read as bounded (P03, W18)
    "a5_design_o1_d1_diff": ("comparative", None, None, M_PTS, 0, "bounded"),
    "a5_design_o1_d2_diff": ("comparative", None, None, M_PTS, 0, "bounded"),
    "a5_design_o1_d4_diff": ("comparative", None, None, M_PTS, 0, "bounded"),
    "a5_design_o1_d5_diff": ("comparative", None, None, M_PTS, 0, "bounded"),
    "a5_m0_o1_d4_diff": ("comparative", None, None, M_PTS, 0, "bounded"),
    "a5_design_o2_gross_d1_diff": ("comparative", None, None, M_BROAD, 0, "bounded"),
    # velocity (C19): the fit explains under the card's floor, so the distance cannot be read
    "vel_z_loglog": ("predictive", None, None, M_Z, 0, "bounded"),
    "vel_z_semilog": ("predictive", None, None, M_Z, 0, "bounded"),
    "vel_z_sl": ("predictive", None, None, M_Z, 0, "bounded"),
    "vel_net_z_loglog": ("predictive", None, None, M_Z, 0, "bounded"),
    "vel_net_z_semilog": ("predictive", None, None, M_Z, 0, "bounded"),
    "vel_net_z_sl": ("predictive", None, None, M_Z, 0, "bounded"),
    # C29 (exploration, written after the grid checks of 2026-10-07): the slope by band of money growth; each band's
    # matters is C29's card's (0.1), fixed before its run
    "lr_x_s1": ("exploration", "lr_x_s1_lo", "lr_x_s1_hi", M_SLOPE, 0, "effect"),
    "lr_x_s2": ("exploration", "lr_x_s2_lo", "lr_x_s2_hi", M_SLOPE, 0, "effect"),  # excludes 0, not inside the size that matters (W18)
    "lr_x_s3": ("exploration", "lr_x_s3_lo", "lr_x_s3_hi", M_SLOPE, 0, "effect"),
    "lr_x_s4": ("exploration", "lr_x_s4_lo", "lr_x_s4_hi", M_SLOPE, 0, "effect"),
    "lr_x_s5": ("exploration", "lr_x_s5_lo", "lr_x_s5_hi", M_SLOPE, 0, "effect"),
}

#: C29's other slices: their type only (an exploration's limits, read beside C28's reading)
EXPLORATION = ("lr_x_s1_gamma", "lr_x_s6_below", "lr_x_s6_above", "lr_x_s7_below", "lr_x_s7_above", "lr_x_s8", "lr_x_s8_below",
               "lr_x_s8_above", "lr_x_s10_below", "lr_x_s10_above", "lr_x_s11_below", "lr_x_s11_above",
               "lr_x_s12_below", "lr_x_s12_above", "lr_x_s13_gamma", "lr_x_s13_below", "lr_x_s13_above",
               "lr_x_s14_share_close", "lr_x_s14_median_gap", "lr_x_s15_separates", "lr_x_s15_theta_share")

#: The measurements a reader sees without a claim on them (C01, C13, the outcomes after a printing): their
#: type only. Description is only described (P05).
DESCRIPTIVE = ("door_w1_prices_pa", "door_w2_prices_pa", "door_w1_added", "door_w2_added", "tax_hh_lower_current",
               "tax_hh_upper_current", "tax_whole_total", "a5_design_o1_med", "a5_design_o1pp_med", "sits_reserves_share")


def labels() -> dict[str, tuple[str, str, str]]:
    """key -> (measure, period, population), for every key a reader's text prints (filled in ``LABELS``)."""
    try:
        from labels import LABELS  # noqa: PLC0415  (the printed keys' labels, written with the forms)
    except ImportError:
        return {}
    return LABELS


def extras(entries: dict) -> None:
    for key, value, unit, fmt in (("matters_slope", M_SLOPE, "points of inflation per point of growth", "{:.2g}"),
                                  ("matters_growth", M_GROWTH, "points of inflation per point of growth", "{:.2g}"),
                                  ("matters_pts", M_PTS, "points of inflation a year", "{:.0f}"),
                                  ("matters_broad", M_BROAD, "points of broad money growth a year", "{:.0f}"),
                                  ("matters_z", M_Z, "standard deviations", "{:.0f}")):
        entries[key] = {"value": value, "unit": unit, "fmt": fmt, "as_of": "2026-10-06",
                        "origin": {"kind": "computed", "script": "code/readings.py"},
                        "note": "a size that matters, set on 2026-10-06 after the results were seen (check/2026-10-06-readings.md)"}
    """The few numbers the regenerated forms add, each computed here from what is already registered or frozen:
    the slope below the line scaled to a ten-point printing (the size the reader meets), and what US prices did
    to a balance left untouched over C13's months (the web study's calculator)."""
    s = entries["lr_base_mu_below"]
    entries["lr_mu_below_x10"] = {
        "value": 10 * s["value"], "unit": "points of inflation a year", "fmt": "{:.1f} points",
        "origin": {"kind": "computed", "script": "code/readings.py (card C28)"}, "as_of": s["as_of"],
        "note": "ten times the slope below the line: ten points more money growth a year, kept up for a decade"}
    import tax  # noqa: PLC0415
    P = tax.monthly_prices("CPIAUCSL", "2026-09-27")
    first, last = entries["door_w2_start"]["value"], entries["tax_last_month"]["value"]
    p0, p1 = float(P[str(first)[:7]]), float(P[str(last)[:7]])
    for key, value, unit, fmt in (("cash_cpi_rise", 100 * (p1 / p0 - 1), "percent", "{:.1f}%"),
                                  ("cash_share_lost", 100 * (1 - p0 / p1), "percent of purchasing power", "{:.1f}%")):
        entries[key] = {"value": value, "unit": unit, "fmt": fmt, "as_of": "2026-09-27",
                        "origin": {"kind": "computed", "script": "code/readings.py (card C13)"}}


def apply(path: Path | None = None) -> None:
    path = path or K.STUDY / "results" / "numbers.json"
    body = json.loads(path.read_text())
    entries = body["numbers"]
    extras(entries)
    for key, (ctype, lo, hi, matters, null, reading) in CLAIMS.items():
        e = entries[key]
        e["claim_type"] = ctype
        if lo:
            e["low"], e["high"] = float(entries[lo]["value"]), float(entries[hi]["value"])
        e["matters"] = matters
        if null:
            e["null"] = null
        if lo:  # a reading is what a range rules out (W18): a key with no range carries none
            e["reading"] = reading
        else:
            e.pop("reading", None)
    for key in DESCRIPTIVE:
        entries[key].setdefault("claim_type", "descriptive")
    for key in EXPLORATION:
        entries[key]["claim_type"] = "exploration"
    for e in entries.values():  # a rule's parameter, cited from its card: the card's name goes to the locator
        o = e.get("origin") or {}
        if o.get("kind") == "cited" and str(o.get("source", "")).startswith("the study's card"):
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
