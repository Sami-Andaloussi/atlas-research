"""The numbers registry: every number the study prints, from the cards' results (``results/runs/``),
written into ``results/numbers.json`` with its unit, origin and as-of date (BLUEPRINT §5 d). Numbers the
study cites (the Federal Reserve's remittances) are entered as cited, with their source and locator.
Called by ``run.py`` after the cards; rerunning it on the same results gives the same registry.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as K  # noqa: E402
import frame_e as F  # noqa: E402
import registry_v15  # noqa: E402

from ft import numbers  # noqa: E402

AS_OF = "2026-09-30"  # the vintage of the frozen series (the CPI's is 2026-09-27, said where it matters)


def load(card: str) -> dict:
    return json.loads((K.RUNS / f"{card}.json").read_text())["result"]


class Reg:
    def __init__(self) -> None:
        self.reg = numbers.Registry.load(K.STUDY / "results" / "numbers.json")
        self.reg.entries.clear()

    def put(self, key: str, value, unit: str, script: str, fmt: str | None = None, **kw) -> None:
        self.reg.put(key, value, unit=unit, origin=numbers.computed(script), as_of=AS_OF, fmt=fmt, **kw)

    def cite(self, key: str, value, unit: str, source: str, locator: str, fmt: str | None = None) -> None:
        self.reg.put(key, value, unit=unit, origin=numbers.cited(source, locator), as_of=AS_OF, fmt=fmt)

    def save(self) -> None:
        self.reg.save()


PCT1 = "{:.1f}%"
PCT0 = "{:.0f}%"
PTS1 = "{:.1f} points"
N0 = "{:,.0f}"


def door(R: Reg) -> None:
    r = load("C01-door")
    s = "code/door.py (card C01)"
    for name, key in (("W1", "w1"), ("W2", "w2"), ("W1-22", "w1_22")):
        w = r["windows"][name]
        R.put(f"door_{key}_start", w["start"], "date", s)
        R.put(f"door_{key}_end", w["end"], "date", s)
        R.put(f"door_{key}_months", w["months"], "months", s)
        R.put(f"door_{key}_base_start", w["B_start_bn"] / 1000, "trillion dollars", s, fmt="${:.2f} trillion")
        R.put(f"door_{key}_base_end", w["B_end_bn"] / 1000, "trillion dollars", s, fmt="${:.2f} trillion")
        R.put(f"door_{key}_added", w["added_bn"] / 1000, "trillion dollars", s, fmt="${:.1f} trillion")
        R.put(f"door_{key}_multiple", w["multiple"], "times", s, fmt="{:.1f} times")
        R.put(f"door_{key}_growth_pa", w["base_growth_pa"], "percent a year", s, fmt=PCT1)
        R.put(f"door_{key}_share_pa", w["added_share_pa"], "percent of the start year's GDP a year", s, fmt=PCT1)
        R.put(f"door_{key}_share_total", w["added_share_total"], "percent of the start year's GDP", s, fmt=PCT1)
        R.put(f"door_{key}_prices_pa", w["prices_pa"], "percent a year", s, fmt=PCT1)
        R.put(f"door_{key}_prices_total", w["prices_total"], "percent", s, fmt=PCT1)
        R.put(f"door_{key}_gdp", w["gdp_start_year_bn"] / 1000, "trillion dollars", s, fmt="${:.2f} trillion")
    ratios = r["ratios_W2_over_W1"]
    R.put("door_ratio_share_pa", ratios["added_share_pa"], "times", s, fmt="{:.1f}")
    R.put("door_ratio_prices_pa", ratios["prices_pa"], "times", s, fmt="{:.1f}")
    R.put("door_ratio_growth_pa", ratios["base_growth_pa"], "times", s, fmt="{:.1f}")


def frame_list(R: Reg) -> None:
    r = load("C15-e-episodes-closed")
    s = "code/frame_e.py (card C15)"
    # The pilot reads the filled prices (plan/e1-production.md, Decisions, "The pilot reads the filled prices"):
    # everything C15's list says that reads the CPI (the accommodation readings, the tested sets, the episodes
    # whose prices cannot be read) is read from C26's re-reading of C15's lists on the filled CPI; the same
    # numbers on the unfilled CPI, C15's own, stay under ``e_u_*`` for the sentences that say them beside.
    c26 = load("C26-a5-deciders-hko-fill")
    assert not c26["void"], "C26's unfilled CPI did not reproduce C15, C18 and C24"
    fr = c26["frame"]["filled"]
    sm_u = r["summary"]
    sm = {**sm_u, **fr["summary"]}
    s26 = "code/gap5_fill.py (card C26)"
    for key, name in (("acc_design", "accommodation_design"), ("acc_m0", "accommodation_m0"),
                      ("acc_design_unread", "accommodation_design_cannot_be_read"), ("tested_design", "tested_design"),
                      ("tested_m0", "tested_m0")):
        R.put(f"e_u_{key}", sm_u[name], "episodes", "code/frame_e.py (card C15)")
    R.put("e_u_unread_kept", c26["frame"]["unfilled"]["unread_kept"], "episodes", s26)
    R.put("e_u_acc_kept", c26["frame"]["unfilled"]["acc_kept"], "episodes", s26)
    R.put("e_episodes", sm["episodes"], "episodes", s)
    R.put("e_moneys", sm["moneys"], "moneys", s)
    R.put("e_moneys_scanned", r["moneys_in_panel"], "moneys", s)
    R.put("e_set_apart", sm["set_apart"], "episodes", s)
    R.put("e_jumps", sm["set_apart_by_kind"].get("one-month jump", 0), "episodes", s)
    R.put("e_definition", sm["set_apart_by_kind"].get("definition change", 0), "episodes", s)
    R.put("e_jump_unread", sm["set_apart_by_kind"].get("jump cannot be read", 0), "episodes", s)
    R.put("e_annual", sm["set_apart_by_kind"].get("annual", 0), "episodes", s)
    R.put("e_censored", sm["censored_at_H"], "episodes", s)
    R.put("e_acc_design", sm["accommodation_design"], "episodes", s26)
    R.put("e_acc_m0", sm["accommodation_m0"], "episodes", s26)
    R.put("e_acc_design_unread", sm["accommodation_design_cannot_be_read"], "episodes", s26)
    R.put("e_tested_design", sm["tested_design"], "episodes", s26)
    R.put("e_tested_m0", sm["tested_m0"], "episodes", s26)
    R.put("e_tested_both", sm["tested_both"], "episodes", s26)
    for i, n in enumerate(sm["tested_design_by_era"]):
        R.put(f"e_tested_design_era{i + 1}", n, "episodes", s26)
    for i, n in enumerate(sm["tested_m0_by_era"]):
        R.put(f"e_tested_m0_era{i + 1}", n, "episodes", s26)
    R.put("e_tested_design_2020", sm["tested_design_2020_2021"], "episodes", s26)
    R.put("e_top_money_share", 100 * sm["top_money_share"], "percent of the list", s, fmt=PCT0)
    R.put("e_seam_tested", sm["seam_in_window_tested_design"], "episodes", s26)
    R.put("e_flagged_tested", sm["flagged_tested_design"], "episodes", s26)
    R.put("e_pool", sm["neither_acc_nor_censored"], "episodes", s26)
    R.put("e_pool_jumps", sm["one_month_jumps_in_that_pool"], "episodes", s26)
    R.put("e_common_end", r["common_end"], "date", s)
    for name in ("smoothing", "X2.5_Y2", "X10_Y2", "H24", "H60"):
        key = name.replace(".", "_")
        R.put(f"e_{key}_episodes", r["sizes"][name]["episodes"], "episodes", s)
        R.put(f"e_{key}_tested", fr["sizes_tested_design"][name], "episodes", s26)
    us = F.from_csv(r["us_episodes"])
    for i, e in enumerate(us, start=1):
        R.put(f"e_us{i}_m0", e["m0"], "date", s)
        R.put(f"e_us{i}_c", e["c"], "date", s)
        R.put(f"e_us{i}_rise", e["rise_pct_gdp"], "percent of the start year's GDP", s, fmt=PCT1)
    R.put("e_us_n", len(us), "episodes", s)
    # the European episodes the text names, and the rule's parameters it prints (cited from the card)
    head = F.from_csv(r["lists"]["headline"])
    # from the list to the tested set, the design's reading (the grid check's G3): the episodes not set
    # apart, the accommodation among them and among those set apart, those whose prices cannot be read
    # from the start to the crossing, and the censored left after them
    kept = [e for e in head if not e["apart_080"]]
    acc = lambda e: str(e["acc_T12"])  # noqa: E731  (True, False or "cannot be read")
    rest = [e for e in kept if acc(e) == "False"]
    R.put("e_kept", len(kept), "episodes", s)
    assert fr["kept"] == len(kept)
    R.put("e_acc_kept", fr["acc_kept"], "episodes", s26)
    R.put("e_acc_apart", fr["acc_apart"], "episodes", s26)
    R.put("e_unread_kept", fr["unread_kept"], "episodes", s26)
    R.put("e_censored_rest", fr["censored_rest"], "episodes", s26)
    assert fr["kept"] - fr["acc_kept"] - fr["unread_kept"] - fr["censored_rest"] == sm["tested_design"]
    for area in ("U2", "GB", "CH", "SE", "JP"):
        eps = [e for e in head if e["area"] == area and e["m0"] >= "2008"]
        kept = [e for e in eps if not e["apart_080"]]
        R.put(f"e_{area.lower()}_n", len(kept), "episodes (not set apart) since 2008", s)
        for i, e in enumerate(eps, start=1):
            R.put(f"e_{area.lower()}{i}_m0", e["m0"], "date", s)
            R.put(f"e_{area.lower()}{i}_rise", e["rise_pct_gdp"], "percent of the start year's GDP", s, fmt=PCT1)
    card = "the study's card C15-e-episodes-closed"
    R.cite("e_X", 5, "percent of a year's GDP", card, "parameters, X_pct_of_gdp", fmt=PCT0)
    R.cite("e_Y", 2, "years", card, "parameters, Y_years", fmt="{:.0f}")
    R.cite("e_T", 12, "percent a year (inflation)", card, "parameters, T_inflation_pct", fmt=PCT0)
    R.cite("e_H", 36, "months", card, "parameters, H_months", fmt="{:.0f}")


def tax(R: Reg) -> None:
    r = load("C13-a6-checked")
    s = "code/tax.py (card C13)"
    R.put("tax_first_month", r["period"]["first_loss_month"], "date", s)
    R.put("tax_last_month", r["period"]["last_month"], "date", s)
    hh = r["households"]
    ph = hh["per_household"]
    for k in ("upper_current", "lower_current", "upper_constant", "lower_constant"):
        R.put(f"tax_hh_{k}", ph[k], "dollars per household", s, fmt="${:,.0f}")
    R.put("tax_hh_range_ratio", hh["range_ratio"], "times", s, fmt="{:.2f}")
    R.put("tax_hh_upper_total", hh["upper_total_bn"], "billion dollars", s, fmt="${:,.0f} billion")
    R.put("tax_hh_lower_total", hh["lower_total_bn"], "billion dollars", s, fmt="${:,.0f} billion")
    R.put("tax_hh_interest", hh["interest_deducted_bn"], "billion dollars", s, fmt="${:,.0f} billion")
    R.put("tax_households", hh["households_last"] / 1000, "million households", s, fmt="{:.0f} million")
    rc = hh["reclassification"]
    R.put("tax_reclass_rise", rc["rise_bn"] / 1000, "trillion dollars", s, fmt="${:.1f} trillion")
    R.put("tax_reclass_other_fall", rc["other_fall_bn"] / 1000, "trillion dollars", s, fmt="${:.1f} trillion")
    w = r["whole_stock"]
    R.put("tax_whole_total", w["total_bn"] / 1000, "trillion dollars", s, fmt="${:.2f} trillion")
    R.put("tax_whole_total_const", w["total_const_bn"] / 1000, "trillion February-2020 dollars", s,
          fmt="${:.2f} trillion")
    R.put("tax_whole_cash", w["cash_bn"], "billion dollars", s, fmt="${:,.0f} billion")
    R.put("tax_whole_deposits", w["deposits_bn"] / 1000, "trillion dollars", s, fmt="${:.1f} trillion")
    R.put("tax_whole_share_period", w["share_of_period_gdp_pct"], "percent of the period's GDP", s, fmt=PCT1)
    for y, v in w["by_year"].items():
        R.put(f"tax_share_{y}", v["share_pct"], "percent of the year's GDP", s, fmt=PCT1)
        R.put(f"tax_loss_{y}", v["loss_bn"], "billion dollars", s, fmt="${:,.0f} billion")
    R.put("tax_stock_start_cash", w["stock_start_bn"]["cash"] / 1000, "trillion dollars", s, fmt="${:.1f} trillion")
    R.put("tax_stock_start_deposits", w["stock_start_bn"]["deposits"] / 1000, "trillion dollars", s,
          fmt="${:.1f} trillion")
    R.put("tax_stock_last_cash", w["stock_last_bn"]["cash"] / 1000, "trillion dollars", s, fmt="${:.1f} trillion")
    R.put("tax_stock_last_deposits", w["stock_last_bn"]["deposits"] / 1000, "trillion dollars", s,
          fmt="${:.1f} trillion")
    v = r["variants"]
    R.put("tax_var_nsa", v["CPI not seasonally adjusted"]["total_bn"] / 1000, "trillion dollars", s,
          fmt="${:.2f} trillion")
    R.put("tax_var_currcir", v["currency in circulation (CURRCIR)"]["total_bn"] / 1000, "trillion dollars", s,
          fmt="${:.2f} trillion")
    R.put("tax_var_m0", v["start at the rule's m0 (2019-11)"]["total_bn"] / 1000, "trillion dollars", s,
          fmt="${:.2f} trillion")
    sg = r["seigniorage"]
    for y, v in sg["by_year"].items():
        R.put(f"seign_currency_{y}", v["currency_rise_bn"], "billion dollars", s, fmt="${:,.0f} billion")
        R.put(f"seign_currency_share_{y}", v["currency_share_pct"], "percent of the year's GDP", s, fmt="{:.2f}%")
        R.put(f"seign_base_{y}", v["base_rise_bn"] / 1000, "trillion dollars", s, fmt="${:.1f} trillion")
        R.put(f"seign_base_share_{y}", v["base_share_pct"], "percent of the year's GDP", s, fmt=PCT1)
    bc = sg["base_created"]
    R.put("base_created", bc["bn"] / 1000, "trillion dollars", s, fmt="${:.1f} trillion")
    R.put("base_created_start", bc["level_start_bn"] / 1000, "trillion dollars", s, fmt="${:.1f} trillion")
    R.put("base_created_last", bc["level_last_bn"] / 1000, "trillion dollars", s, fmt="${:.1f} trillion")
    R.put("base_created_to", bc["to"], "date", s)
    da = r["deferred_asset"]  # RESPPLLOPNWW is in millions of dollars, negative when an asset
    R.put("deferred_lowest", -da["lowest_mn"] / 1000, "billion dollars", s, fmt="${:,.0f} billion")
    R.put("deferred_lowest_date", da["lowest_date"], "date", s)
    R.put("deferred_latest", -da["latest_mn"] / 1000, "billion dollars", s, fmt="${:,.0f} billion")
    R.put("deferred_latest_date", da["latest_date"], "date", s)
    wb = r["where_the_base_sits"]  # WRESBAL and WCURCIR are in millions of dollars (the keys say _bn)
    R.put("sits_week", wb["week"], "date", s)
    R.put("sits_reserves", wb["reserves_bn"] / 1e6, "trillion dollars", s, fmt="${:.1f} trillion")
    R.put("sits_currency", wb["currency_bn"] / 1e6, "trillion dollars", s, fmt="${:.1f} trillion")
    R.put("sits_reserves_share", wb["reserves_share_pct"], "percent of the base", s, fmt=PCT0)
    R.put("sits_currency_share", wb["currency_share_pct"], "percent of the base", s, fmt=PCT0)


def remittances(R: Reg) -> None:
    """The Board's January releases (notes/fed-statements.md): cited, never computed."""
    src = "Board of Governors of the Federal Reserve System, press release of"
    for key, value, day, url in (
        ("remit_2020", 88.5, "11 January 2021", "other20210111a"),
        ("remit_2021", 107.4, "14 January 2022", "other20220114a"),
        ("remit_2022", 76.0, "13 January 2023", "other20230113a"),
        ("deferred_2022", 18.8, "13 January 2023", "other20230113a"),
        ("loss_2023", 114.3, "12 January 2024", "other20240112a"),
        ("deferred_2023", 133.0, "12 January 2024", "other20240112a"),
        ("ior_expense_2020", 7.9, "11 January 2021", "other20210111a"),
        ("ior_expense_2021", 5.3, "14 January 2022", "other20220114a"),
        ("ior_rise_2022", 55.1, "13 January 2023", "other20230113a"),
        ("ior_rise_2023", 116.3, "12 January 2024", "other20240112a"),
    ):
        R.cite(key, value, "billion dollars", f"{src} {day} (preliminary, unaudited)",
               f"https://www.federalreserve.gov/newsevents/pressreleases/{url}.htm", fmt="${:.1f} billion")


def velocity(R: Reg) -> None:
    r = load("C19-velocity-bare")
    s = "code/velocity.py (card C19)"
    for form, key in (("log-log", "loglog"), ("semi-log", "semilog"), ("Selden-Latane", "sl")):
        f = r["m2"][form]
        R.put(f"vel_r2_{key}", 100 * f["r2"], "percent of velocity's variance", s, fmt=PCT1)
        R.put(f"vel_z_{key}", f["z"], "standard deviations", s, fmt="{:.1f}")
        R.put(f"vel_net_z_{key}", r["m2net"][form]["z"], "standard deviations", s, fmt="{:.1f}")
    R.cite("vel_r2_floor", 30, "percent of velocity's variance", "the study's card C19-velocity-bare",
           "parameters, min_in_sample_r2 (C07's floor)", fmt=PCT0)
    R.put("vel_n_fit", r["m2"]["Selden-Latane"]["n_fit"], "quarters", s)
    R.put("vel_n_test", r["m2"]["Selden-Latane"]["n_test"], "quarters", s)
    R.put("vel_first_episode", r["cutoff"]["first_us_episode_m0"], "date", s)
    R.put("vel_purchases", r["purchases_since_cutoff_bn_last"] / 1000, "trillion dollars", s, fmt="${:.1f} trillion")
    path = r["m2"]["Selden-Latane"]["path"]["actual"]
    cut = r["cutoff"]["fit_last_quarter"]
    after = {q: v for q, v in path.items() if q > cut}
    low = min(after, key=after.get)
    R.put("vel_at_cut", path[cut], "dollars of GDP per dollar of M2", s, fmt="{:.2f}")
    R.put("vel_low", after[low], "dollars of GDP per dollar of M2", s, fmt="{:.2f}")
    R.put("vel_low_quarter", f"{low[:4]}-{int(low[-1]) * 3:02d}", "date", s, fmt="%B %Y")
    last = max(path)
    R.put("vel_last", path[last], "dollars of GDP per dollar of M2", s, fmt="{:.2f}")
    R.put("vel_last_quarter", f"{last[:4]}-{int(last[-1]) * 3:02d}", "date", s, fmt="%B %Y")
    R.put("vel_before_max", max(v for q, v in path.items() if q <= cut), "dollars of GDP per dollar of M2", s,
          fmt="{:.2f}")
    cm = r["cross_money"]
    R.put("vel_cross_n", len(cm["moneys"]), "moneys", s)
    for verdict, key in (("fell below", "below"), ("fit cannot tell", "cannot"),
                         ("moved as the rate predicts", "as_rate"), ("between", "between")):
        R.put(f"vel_cross_{key}", cm["by_money_verdict"].get(verdict, 0), "moneys", s)
    R.cite("vel_min_years", 20, "years of data before the first printing", "the study's card C19-velocity-bare",
           "method (2), inherited from C07", fmt="{:.0f}")
    x = r["variants"]["cutoff from C15's list X10_Y2 (2020-02)"]["log-log"]
    R.put("vel_x10_r2", 100 * x["r2"], "percent of velocity's variance", s, fmt=PCT0)
    # the best fit of the three forms in the M1 and opportunity-cost variants (all "fit cannot tell")
    for name, key in (("M1 (test to 2020Q1)", "m1"), ("opportunity cost r - M2OWN (fit and test to 2019Q2)", "own")):
        R.put(f"vel_{key}_r2_max", 100 * max(f["r2"] for f in r["variants"][name].values()),
              "percent of velocity's variance", s, fmt=PCT1)


def _a4_summary(r: dict) -> dict:
    """A C02-shaped stored run (C02, C03) as C25's summary shape."""
    h, ho = r["headline"], r["held_out"]
    return {"windows": h["n"], "moneys": h["moneys"], "beta": h["beta"], "lo": h["beta_lo"], "hi": h["beta_hi"],
            "r2": h["r2"], "gamma": h["coef"]["g"]["b"], "gamma_lo": h["coef"]["g"]["lo"], "gamma_hi": h["coef"]["g"]["hi"],
            "line_pi": r["prior_line_on_pi"], "line_mu": r["prior_line_on_mu"], "folds_differing": ho["folds_differing"],
            "held_out": {"train_windows": ho["train_windows"], "test_windows": ho["test_windows"],
                         "moneys_in_both": ho["moneys_in_both"], "oos_r2": ho["oos_r2"], "beta": ho["test"]["beta"],
                         "lo": ho["test"]["beta_lo"], "hi": ho["test"]["beta_hi"],
                         "fit_train_beta": ho["fit_train"]["beta"]}}


def _put_a4(R: Reg, key: str, f: dict, s: str, f3: bool = False) -> None:
    PP = "points of inflation per point of money growth"
    R.put(f"{key}_n", f["windows"], "decade windows", s)
    R.put(f"{key}_moneys", f["moneys"], "moneys", s)
    R.put(f"{key}_beta", f["beta"], PP, s, fmt="{:.2f}")
    R.put(f"{key}_lo", f["lo"], PP, s, fmt="{:.2f}")
    R.put(f"{key}_hi", f["hi"], PP, s, fmt="{:.2f}")
    R.put(f"{key}_r2", 100 * f["r2"], "percent", s, fmt=PCT0)
    for way in ("pi", "mu"):
        p = f[f"line_{way}"]
        for side in ("below", "above"):
            R.put(f"{key}_{way}_{side}", p[f"beta_{side}"], "points per point", s, fmt="{:.2f}")
            R.put(f"{key}_{way}_{side}_lo", p[f"beta_{side}_lo"], "points per point", s, fmt="{:.2f}")
            R.put(f"{key}_{way}_{side}_hi", p[f"beta_{side}_hi"], "points per point", s, fmt="{:.2f}")
            R.put(f"{key}_{way}_{side}_n", p[f"windows_{side}"], "decade windows", s)
    ho = f["held_out"]
    R.put(f"{key}_ho_train", ho["train_windows"], "decade windows", s)
    R.put(f"{key}_ho_test", ho["test_windows"], "decade windows", s)
    R.put(f"{key}_ho_moneys", ho["moneys_in_both"], "moneys", s)
    R.put(f"{key}_ho_r2", 100 * ho["oos_r2"], "percent", s, fmt=PCT0)
    R.put(f"{key}_ho_beta", ho["beta"], "points per point", s, fmt="{:.2f}")
    f3s = "{:.3f}" if f3 else "{:.2f}"  # broad money's interval misses one by 0.003
    R.put(f"{key}_ho_lo", ho["lo"], "points per point", s, fmt=f3s)
    R.put(f"{key}_ho_hi", ho["hi"], "points per point", s, fmt=f3s)
    R.put(f"{key}_ho_train_beta", ho["fit_train_beta"], "points per point", s, fmt="{:.2f}")
    R.put(f"{key}_folds_differing", f["folds_differing"], "folds", s)
    for suffix, v in (("gamma", f["gamma"]), ("gamma_lo", f["gamma_lo"]), ("gamma_hi", f["gamma_hi"])):
        R.put(f"{key}_{suffix}", v, "points of inflation per point of output growth", s, fmt="{:.2f}")


def longrun(R: Reg) -> None:
    """C02 and C03. The pilot reads the filled prices: ``lr_base_*`` is C25's run (C02's model with the CPI gaps
    filled), the same numbers on the unfilled panel, C02's own, stay under ``lr_base_u_*`` for the sentences that
    say them beside. C02's variants, its window from 2020 and C03 were not rerun with the fill: they stay C02's and
    C03's, on the unfilled panel, under ``lr_base_2020_*``, ``lr_base_yield_*`` and ``lr_broad_2020_*`` / ``lr_broad_yield_*``.
    C03 itself was rerun with the fill as card C27 (C03's child, C25's rule unchanged): ``lr_broad_*`` is C27's run,
    C03's own, on the unfilled panel, stays under ``lr_broad_u_*``."""
    c25 = load("C25-a4-base-hko-fill")
    assert not c25["void"], "C25's unfilled panel did not reproduce C02 and C22"
    s25 = "code/gap5_fill.py (card C25)"
    c28 = load("C28-a4-units-guard")  # the regeneration's correction: C25 and C27 with the units guard (2026-10-07)
    assert not c28["void"], "C28 did not reproduce C25 and C27 with its guard off"
    s28 = "code/units_guard.py (card C28)"
    _put_a4(R, "lr_base", c28["C02_grid"]["guarded"], s28)
    _put_a4(R, "lr_c25", c25["C02_grid"]["filled"], s25)
    _put_a4(R, "lr_base_u", _a4_summary(load("C02-a4-base")), "code/longrun.py (card C02)")
    R.put("lr_fill_c02_added", c25["C02_grid"]["n_added"], "decade windows", s25)
    c27 = load("C27-a4-broad-hko-fill")
    assert not c27["void"], "C27's unfilled panel did not reproduce C03"
    s27 = "code/gap5_fill.py (card C27)"
    _put_a4(R, "lr_broad", c28["broad"]["guarded"], s28, f3=True)
    _put_a4(R, "lr_c27", c27["filled"], s27, f3=True)
    R.put("lr_guard_switched", len(c28["switched"]["rgdp"]), "economies", s28)
    bf = {(w["area"], w["y0"]): w for w in c28["C02_grid"]["windows_changed"]}[("BF", 1970)]
    R.put("lr_guard_bf_g_old", bf["g_off"], "percent a year, ten-year average", s28, fmt=PCT0)
    R.put("lr_guard_bf_g_new", bf["g_on"], "percent a year, ten-year average", s28, fmt=PCT1)
    R.put("lr_fill_c03_added", c27["n_added"], "decade windows", s27)
    R.put("lr_fill_c03_added_economies", len({w["area"] for w in c27["windows_added"]}), "economies", s27)
    R.put("lr_fill_c03_moneys_added", len(c27["moneys_added"]), "moneys", s27)
    R.put("lr_fill_c03_lost_before", c27["lost_for_missing_cpi"]["unfilled"], "decade windows", s27)
    R.put("lr_fill_c03_lost_after", c27["lost_for_missing_cpi"]["filled"], "decade windows", s27)
    R.put("lr_fill_c03_lost_after_pre1970", c27["lost_for_missing_cpi"]["filled_starting_before_1970"], "decade windows", s27)
    b27 = c27["beside_base_money"]
    R.put("lr_common", b27["common_windows"], "decade windows", s27)
    R.put("lr_broad_common_beta", b27["beta_broad_common"], "points per point", s27, fmt="{:.2f}")
    R.put("lr_base_common_beta", b27["beta_base_common"], "points per point", s27, fmt="{:.2f}")
    R.put("lr_broad_fold_partly", sum(f["verdict"] != c27["filled"]["verdict"] for f in c27["filled"]["folds"]), "folds", s27)
    for card, key in (("C02-a4-base", "lr_base"), ("C03-a4-broad", "lr_broad")):
        r = load(card)
        s = f"code/longrun.py (card {card.split('-')[0]})"
        if key == "lr_broad":
            _put_a4(R, "lr_broad_u", _a4_summary(r), s, f3=True)
        h = r["headline"]
        f20 = r["from_2020"]
        R.put(f"{key}_2020_to", f20["to"], "year", s, fmt="{}")
        R.put(f"{key}_2020_n", f20["n"], "moneys", s)
        R.put(f"{key}_2020_beta", f20["beta"], "points per point", s, fmt="{:.2f}")
        R.put(f"{key}_2020_lo", f20["beta_lo"], "points per point", s, fmt="{:.2f}")
        R.put(f"{key}_2020_hi", f20["beta_hi"], "points per point", s, fmt="{:.2f}")
        yc = r["variants"]["yield correction (rates at least 1% at both ends)"]
        R.put(f"{key}_yield_beta", yc["beta"], "points per point", s, fmt="{:.2f}")
        R.put(f"{key}_yield_lo", yc["beta_lo"], "points per point", s, fmt="{:.2f}")
        R.put(f"{key}_yield_hi", yc["beta_hi"], "points per point", s, fmt="{:.2f}")
        R.put(f"{key}_yield_n", yc["n"], "decade windows", s)
    R.cite("lr_line", 12, "percent a year", "Teles and Uhlig, 'Is quantity theory still alive?', working paper",
           "pp. 3 and 11 (notes/sources.md)", fmt=PCT0)
    R.put("lr_dropped", len(load("C02-a4-base")["sample"]["moneys_dropped_units_break"]), "moneys",
          "code/longrun.py (card C02)")
    R.cite("lr_ci", 95, "percent (interval)", "the study's card C02-a4-base", "parameters, interval", fmt=PCT0)
    R.put("lr_folds", len(load("C02-a4-base")["held_out"]["folds"]), "groups of currencies",
          "code/longrun.py (card C02)")
    b = load("C03-a4-broad")["beside_C02"]
    R.put("lr_common_u", b["common_windows"], "decade windows", "code/longrun.py (card C03)")
    # single windows the text names (C02's points: ten-year averages of base money growth and inflation)
    pts = {(p["area"], p["y0"]): p for p in load("C02-a4-base")["points"]}
    for area, y0 in (("U2", 2010), ("GB", 2010), ("SE", 2010), ("JP", 2010), ("US", 2010), ("US", 2000)):
        p = pts[(area, y0)]
        for v in ("mu", "pi"):
            R.put(f"lr_pt_{area.lower()}_{y0}_{v}", p[v], "percent a year, ten-year average",
                  "code/longrun.py (card C02)", fmt=PCT1)


def explore(R: Reg) -> None:
    """C29 (exploration, C28's child, written after the grid checks of 2026-10-07): every slice the card named."""
    r = load("C29-a4-exploration-pace")
    s = "code/units_guard.py (card C29)"
    PP = "points of inflation per point of money growth"
    for i, k in enumerate(("S1_band_le12", "S2_band_12_20", "S3_band_20_30", "S4_band_30_50", "S5_band_gt50"), 1):
        b = r[k]
        for suffix, v in (("", b["beta"]), ("_lo", b["lo"]), ("_hi", b["hi"])):
            R.put(f"lr_x_s{i}{suffix}", v, PP, s, fmt="{:.2f}")
        R.put(f"lr_x_s{i}_n", b["windows"], "decade windows", s)
    lines = {6: r["S6_above_line_without_gt30"], 7: r["S7_from_2000"], 8: r["S8_outside_1970_2000"]["line"],
             10: r["S10_without_unions"]["line"], 11: r["S11_cluster_by_union"], 12: r["S12_without_shrinking_base"]["line"],
             13: r["S13_g_from_world_bank"]["line"]}
    for i, p in lines.items():
        for side in ("below", "above"):
            for suffix, v in (("", p[f"beta_{side}"]), ("_lo", p[f"beta_{side}_lo"]), ("_hi", p[f"beta_{side}_hi"])):
                R.put(f"lr_x_s{i}_{side}{suffix}", v, PP, s, fmt="{:.2f}")
            R.put(f"lr_x_s{i}_{side}_n", p[f"windows_{side}"], "decade windows", s)
    b1 = r["S1_band_le12"]  # output growth's slope at or below the line (the confirming check's N2)
    for suffix, v in (("gamma", b1["gamma"]), ("gamma_lo", b1["gamma_lo"]), ("gamma_hi", b1["gamma_hi"])):
        R.put(f"lr_x_s1_{suffix}", v, "points of inflation per point of output growth", s, fmt="{:.2f}")
    o = r["S8_outside_1970_2000"]["pooled"]
    for suffix, v in (("", o["beta"]), ("_lo", o["lo"]), ("_hi", o["hi"])):
        R.put(f"lr_x_s8{suffix}", v, PP, s, fmt="{:.2f}")
    R.put("lr_x_s8_n", o["windows"], "decade windows", s)
    R.put("lr_x_s10_moneys", r["S10_without_unions"]["moneys_left"], "economies", s)
    R.put("lr_x_s12_dropped", len(r["S12_without_shrinking_base"]["windows_dropped"]), "decade windows", s)
    g = r["S13_g_from_world_bank"]["pooled"]
    for suffix, v in (("gamma", g["gamma"]), ("gamma_lo", g["gamma_lo"]), ("gamma_hi", g["gamma_hi"])):
        R.put(f"lr_x_s13_{suffix}", v, "points of inflation per point of output growth", s, fmt="{:.2f}")
    lv = r["S14_levels"]
    R.put("lr_x_s14_share_close", 100 * lv["share_above_within_3_or_more"], "percent of decade windows above the line", s, fmt=PCT0)
    R.put("lr_x_s14_median_gap", lv["median_gap_above"], "points a year", s, fmt="{:.1f}")
    n = r["S15_null"]
    R.put("lr_x_s15_separates", 100 * n["share_separates"], "percent of draws", s, fmt=PCT1)
    R.put("lr_x_s15_theta_share", 100 * n["share_theta_at_least_observed"], "percent of draws", s, fmt=PCT1)
    R.put("lr_x_s15_draws", n["draws"], "draws", s)
    for edge in (20, 30, 50):  # the bands' edges, named on C29's card before its run (the checkers' cuts)
        R.cite(f"lr_x_edge{edge}", edge, "percent a year", "the study's card C29-a4-exploration-pace", "slices, the bands",
               fmt=PCT0)


def longrun_1870(R: Reg) -> None:
    """C21 (C04 with the real GDP per capita column its card names): 1870-1950, 18 economies."""
    r = load("C21-a4-1870-named")
    s = "code/longrun.py (card C21)"
    PP = "points of inflation per point of money growth"
    R.put("lr_1870_n", r["sample"]["windows"], "decade windows", s)
    R.put("lr_1870_economies", r["sample"]["economies"], "economies", s)
    h = r["headline"]
    for suffix, v in (("beta", h["beta"]), ("lo", h["beta_lo"]), ("hi", h["beta_hi"])):
        R.put(f"lr_1870_{suffix}", v, PP, s, fmt="{:.2f}")
    g = h["coef"]["g"]
    for suffix, v in (("gamma", g["b"]), ("gamma_lo", g["lo"]), ("gamma_hi", g["hi"])):
        R.put(f"lr_1870_{suffix}", v, "points of inflation per point of output growth", s, fmt="{:.2f}")
    R.put("lr_1870_r2", 100 * h["r2"], "percent", s, fmt=PCT0)
    R.put("lr_1870_oos_r2", 100 * r["out_of_sample"]["oos_r2_from_C02"], "percent", s, fmt=PCT0)
    for way in ("pi", "mu"):
        p = r[f"prior_line_on_{way}"]
        for side in ("below", "above"):
            R.put(f"lr_1870_{way}_{side}", p[f"beta_{side}"], "points per point", s, fmt="{:.2f}")
            R.put(f"lr_1870_{way}_{side}_lo", p[f"beta_{side}_lo"], "points per point", s, fmt="{:.2f}")
            R.put(f"lr_1870_{way}_{side}_hi", p[f"beta_{side}_hi"], "points per point", s, fmt="{:.2f}")
            R.put(f"lr_1870_{way}_{side}_n", p[f"windows_{side}"], "decade windows", s)
    R.put("lr_1870_folds_one", sum(f["verdict"] == "one for one" for f in r["folds"]), "folds", s)
    R.put("lr_1870_folds", len(r["folds"]), "folds", s)
    R.put("lr_1870_folds_differing", sum(f["verdict"] != h["verdict"] for f in r["folds"]), "folds", s)
    for name, key in (("broad money", "broad"), ("world-war windows apart", "nowar"), ("five-year windows", "five")):
        v = r["variants"][name]
        for suffix, x in (("beta", v["beta"]), ("lo", v["beta_lo"]), ("hi", v["beta_hi"])):
            R.put(f"lr_1870_{key}_{suffix}", x, "points per point", s, fmt="{:.2f}")
        R.put(f"lr_1870_{key}_n", v["n"], "windows", s)
    o = r["overlap_1950_2020"]
    for part, key in (("jst_1950_2020", "ov_jst"), ("panel_same_economies", "ov_panel")):
        v = o[part]
        for suffix, x in (("beta", v["beta"]), ("lo", v["beta_lo"]), ("hi", v["beta_hi"])):
            R.put(f"lr_1870_{key}_{suffix}", x, "points per point", s, fmt="{:.2f}")
        R.put(f"lr_1870_{key}_n", v["moneys"], "economies", s)


def _put_c22(R: Reg, key: str, f: dict, s: str) -> None:
    PP = "points of inflation per point of money growth"
    R.put(f"{key}_n", f["windows"], "decade windows", s)
    R.put(f"{key}_moneys", f["moneys"], "moneys", s)
    for suffix, v in (("beta", f["beta"]), ("lo", f["lo"]), ("hi", f["hi"])):
        R.put(f"{key}_{suffix}", v, PP, s, fmt="{:.2f}")
    for way in ("pi", "mu"):
        p = f[f"line_{way}"]
        for side in ("below", "above"):
            R.put(f"{key}_{way}_{side}", p[f"beta_{side}"], "points per point", s, fmt="{:.2f}")
            R.put(f"{key}_{way}_{side}_lo", p[f"beta_{side}_lo"], "points per point", s, fmt="{:.2f}")
            R.put(f"{key}_{way}_{side}_hi", p[f"beta_{side}_hi"], "points per point", s, fmt="{:.2f}")
    ho = f["held_out"]
    R.put(f"{key}_ho_beta", ho["beta"], "points per point", s, fmt="{:.2f}")
    R.put(f"{key}_ho_lo", ho["lo"], "points per point", s, fmt="{:.2f}")
    R.put(f"{key}_ho_hi", ho["hi"], "points per point", s, fmt="{:.2f}")
    R.put(f"{key}_folds_differing", f["folds_differing"], "folds", s)
    R.put(f"{key}_folds", 5, "folds", s)
    for suffix, v in (("gamma", f["gamma"]), ("gamma_lo", f["gamma_lo"]), ("gamma_hi", f["gamma_hi"])):
        R.put(f"{key}_{suffix}", v, "points of inflation per point of output growth", s, fmt="{:.2f}")


def longrun_2019(R: Reg) -> None:
    """C22 (C02's model on decades ending in December 2019), read beside C02. The pilot reads the filled prices:
    ``lr_c22_*`` is C25's run on C22's grid, C22's own run (the unfilled panel) stays under ``lr_c22_u_*``; the five
    named points are windows the fill does not touch (the same in both)."""
    r = load("C22-a4-base-2019-narrowed")
    c25 = load("C25-a4-base-hko-fill")
    s25 = "code/gap5_fill.py (card C25)"
    c28 = load("C28-a4-units-guard")
    s28 = "code/units_guard.py (card C28)"
    s = "code/longrun.py (card C22)"
    _put_c22(R, "lr_c22", c28["C22_grid"]["guarded"], s28)
    _put_c22(R, "lr_c22_c25", c25["C22_grid"]["filled"], s25)
    uf = c25["C22_grid"]["unfilled"]
    _put_c22(R, "lr_c22_u", uf, s25)
    assert abs(uf["beta"] - r["headline"]["beta"]) < 1e-9, "C25's unfilled C22 grid is not C22's run"
    R.put("lr_fill_c22_added", c25["C22_grid"]["n_added"], "decade windows", s25)
    for p in r["named_points"]:
        pt = p["c22_2009_2019"]
        for v in ("mu", "pi"):
            R.put(f"lr_c22_pt_{p['area'].lower()}_{v}", pt[v], "percent a year, ten-year average", s, fmt=PCT1)
        cp = {(w["area"], w["y1"]): w for w in c28["C22_grid"]["points"]}[(p["area"], 2019)]
        assert abs(cp["mu"] - pt["mu"]) < 1e-3 and abs(cp["pi"] - pt["pi"]) < 1e-3, "a named point moved under the fill"
    cz = {(w["area"], w["y1"]): w for w in c28["C22_grid"]["points"]}[("CZ", 2019)]  # Czechia, named by grid check A
    for v in ("mu", "pi"):
        R.put(f"lr_c22_pt_cz_{v}", cz[v], "percent a year, ten-year average", s28, fmt=PCT1)


def longrun_dgp(R: Reg) -> None:
    """C23 (C02's model with De Grauwe and Polan's 10% line, from their abstract), read beside Teles and
    Uhlig's 12% in C02."""
    r = load("C23-a4-base-de-grauwe-polan")
    s = "code/longrun.py (card C23)"
    R.cite("lr_dgp_line", 10, "percent a year", "De Grauwe and Polan, CEPR Discussion Paper 2841 (2001), abstract",
           "'low inflation countries (on average less than 10% per annum over the last 30 years)'; "
           "data/cepr/dp2841/2026-10-01", fmt=PCT0)
    R.cite("lr_dgp_years", 30, "years", "De Grauwe and Polan, CEPR Discussion Paper 2841 (2001), abstract",
           "'on average less than 10% per annum over the last 30 years'; data/cepr/dp2841/2026-10-01", fmt="{:.0f}")
    for name, key, unit in (("headline", "head", "decade windows"), ("variant_A_c22_grid", "a", "decade windows"),
                            ("variant_B_thirty_years", "b", "moneys"), ("outside_1970_2000", "out", "decade windows")):
        v = r[name]
        R.put(f"lr_dgp_{key}_n", v["n"], unit, s)
        R.put(f"lr_dgp_{key}_moneys", v["moneys"], "moneys", s)
        for way in ("pi", "mu"):
            p = v[f"line_on_{way}"]
            for side in ("below", "above"):
                R.put(f"lr_dgp_{key}_{way}_{side}", p[f"beta_{side}"], "points per point", s, fmt="{:.2f}")
                R.put(f"lr_dgp_{key}_{way}_{side}_lo", p[f"beta_{side}_lo"], "points per point", s, fmt="{:.2f}")
                R.put(f"lr_dgp_{key}_{way}_{side}_hi", p[f"beta_{side}_hi"], "points per point", s, fmt="{:.2f}")
                R.put(f"lr_dgp_{key}_{way}_{side}_n", p[f"windows_{side}"], unit, s)
    c = r["variant_C_money_classified"]
    p = c["line_on_money"]
    for side in ("below", "above"):
        R.put(f"lr_dgp_c_{side}", p[f"beta_{side}"], "points per point", s, fmt="{:.2f}")
        R.put(f"lr_dgp_c_{side}_lo", p[f"beta_{side}_lo"], "points per point", s, fmt="{:.2f}")
        R.put(f"lr_dgp_c_{side}_hi", p[f"beta_{side}_hi"], "points per point", s, fmt="{:.2f}")
        R.put(f"lr_dgp_c_{side}_n", p[f"windows_{side}"], "decade windows", s)
    R.put("lr_dgp_c_moneys_high", c["moneys_high"], "moneys", s)
    R.put("lr_dgp_c_moneys_low", c["moneys_low"], "moneys", s)
    ho = r["outside_1970_2000"]["headline"]
    for suffix, v in (("beta", ho["beta"]), ("beta_lo", ho["beta_lo"]), ("beta_hi", ho["beta_hi"])):
        R.put(f"lr_dgp_out_{suffix}", v, "points per point", s, fmt="{:.2f}")
    R.put("lr_dgp_between_pi", r["windows_between_10_and_12"]["pi"], "decade windows", s)
    R.put("lr_dgp_inside", r["sample"]["windows_inside_1970_2000"], "decade windows", s)
    R.put("lr_dgp_outside", r["sample"]["windows_outside_1970_2000"], "decade windows", s)
    tu = r["teles_uhlig_12_from_C02"]["pi"]
    R.put("lr_dgp_tu_pi_below", tu["beta_below"], "points per point", s, fmt="{:.2f}")
    R.put("lr_dgp_tu_pi_above", tu["beta_above"], "points per point", s, fmt="{:.2f}")


def deciders(R: Reg, r: dict | None = None, pre: str = "a5", s: str = "code/deciders.py (card C18)") -> None:
    """C18, or C26 (the same with the CPI gaps filled) as ``_c26_as_c18`` shapes it; ``pre`` is the keys' prefix:
    ``a5`` for the run the text reads, ``a5_u`` for the unfilled one, said beside."""
    r = r or load("C18-a5-deciders-bare")
    filled = pre == "a5"
    h = r["headline"]
    PTS = "{:+.1f} points"
    for reading in ("design", "m0"):
        for o in ("O1", "O2_net", "O2_gross"):
            for d in ("D1", "D2", "D4", "D5"):
                t = h["readings"][reading]["tests"][o][d]
                k = f"{pre}_{reading}_{o.lower()}_{d.lower()}"
                if not t["tested"]:
                    continue
                R.put(f"{k}_coded", t["n_coded"], "episodes", s)
                R.put(f"{k}_n1", t["n1"], "episodes", s)
                R.put(f"{k}_n0", t["n0"], "episodes", s)
                unit = "points a year" if o == "O1" else "percent a year of the starting stock"
                R.put(f"{k}_med1", t["median1"], unit, s, fmt="{:.1f}" if o == "O1" else PCT1)
                R.put(f"{k}_med0", t["median0"], unit, s, fmt="{:.1f}" if o == "O1" else PCT1)
                R.put(f"{k}_diff", t["diff"], unit, s, fmt=PTS)
                R.put(f"{k}_p", t["p_holm"], "p-value after Holm", s, fmt="{:.2f}")
    # D2: every episode at the floor falls in 2000-2026 (the thin reading's strata)
    st = h["readings"]["design"]["tests"]["O1"]["D2"]["strata"]
    R.put(f"{pre}_floor_before_2000", sum(x["n0"] for x in st if x["stratum"] < 2), "episodes", s)
    R.put(f"{pre}_floor_after_2000", sum(x["n0"] for x in st if x["stratum"] == 2), "episodes", s)
    # the share of tested printings followed by lower inflation (O1 below zero; none equals zero), the
    # grid check's G2; and the channel read past the crossing (G4), with its counted variant
    o1 = [e["O1"] for e in r["episodes"] if e["tested_design"] and e["O1"] is not None]
    R.put(f"{pre}_design_o1_down", 100 * sum(x < 0 for x in o1) / len(o1), "percent of episodes", s, fmt=PCT0)
    R.put(f"{pre}_design_o1_p25_fall", -r["what_happened"]["design"]["O1"]["p25"], "points a year", s,
          fmt="{:.1f}")
    R.put(f"{pre}_d4_past_c", sum(1 for e in r["episodes"] if e["tested_design"] and e["past_c"]
                             and e["cat_D4"] is not None), "episodes", s)
    tt = r["two_thirds"]["O1"]["D4"]
    R.put(f"{pre}_d4_k", tt["k"], "counted runs", s)
    R.put(f"{pre}_d4_n", tt["n"], "counted runs", s)
    # the same count for the exchange rate and the deficit (read from the run, as D4's; the reader panel's P4)
    for d in ("D1", "D5"):
        tt = r["two_thirds"]["O1"][d]
        R.put(f"{pre}_{d.lower()}_k", tt["k"], "counted runs", s)
        R.put(f"{pre}_{d.lower()}_n", tt["n"], "counted runs", s)
    R.put(f"{pre}_counted", len(r["counted"]), "counted runs", s)
    x25 = [n for n, v in r["counted"].items() if n.startswith("list X2.5")
           and v["combined"]["O1"]["D4"]["verdict"] == "separates"]
    R.put(f"{pre}_d4_x25_separate", len(x25), "counted runs", s)
    co = max(max(p["same"], p["opposite"]) for rd in r["coincidence"].values() for p in rd.values())
    R.put(f"{pre}_coincide_max", 100 * co, "percent of episodes", s, fmt=PCT0)
    for reading in ("design", "m0"):
        w = r["what_happened"][reading]
        for o, key in (("O1", "o1"), ("O1pp", "o1pp"), ("O2_gross", "o2g"), ("O2_net", "o2n"), ("O3", "o3")):
            q = w[o]
            k = f"{pre}_{reading}_{key}"
            if o == "O3":
                R.put(f"{k}_med", 100 * q["median"], "percent of the rise withdrawn", s, fmt=PCT0)
                continue
            f = "{:.1f}" if o == "O1" else PCT1
            unit = "points a year" if o == "O1" else "percent a year"
            R.put(f"{k}_med", q["median"], unit, s, fmt=f)
            R.put(f"{k}_p25", q["p25"], unit, s, fmt=f)
            R.put(f"{k}_p75", q["p75"], unit, s, fmt=f)
            R.put(f"{k}_n", q["n"], "episodes", s)
            R.put(f"{k}_up", 100 * q["share_above_zero"], "percent of episodes", s, fmt=PCT0)
    if not filled:
        return
    card = "the study's cards C06 and C18 (C18 keeps C06's thresholds)"
    for key, value, unit, loc, fmt in (
        ("a5_perms", 10000, "permutations", "C18 parameters, permutations", "{:,.0f}"),
        ("a5_coincide_threshold", 80, "percent of episodes", "C18 failure clause", PCT0),
        ("a5_min_cat", 3, "episodes per group in a stratum", "C18 parameters, min_per_category_per_stratum", "{:.0f}"),
        ("a5_band", 2, "percent (peg band)", "C06 method, D1: a band of 2% over 12 months", PCT0),
        ("a5_floor", 0.5, "percent a year (the floor)", "C06 method, D2: at or below 0.5%", PCT1),
        ("a5_deficit", 5, "percent of GDP (deficit)", "C06 method, D5: net lending at or below -5% of GDP", PCT0),
    ):
        R.cite(key, value, unit, card, loc, fmt=fmt)
    ac = r["accommodation_apart"]
    R.put(f"{pre}_acc_n", ac["n"], "episodes", s)
    R.put(f"{pre}_acc_o1", ac["O1_median"], "points a year", s, fmt="{:.1f}")
    for row in r["described_us_euro"]:
        k = f"a5_{row['area'].lower()}_{row['m0'][:4]}"
        R.put(f"{k}_m0", row["m0"], "date", s)
        R.put(f"{k}_before", row["O1pp"] - row["O1"], "percent a year", s, fmt=PCT1)
        R.put(f"{k}_after", row["O1pp"], "percent a year", s, fmt=PCT1)
        R.put(f"{k}_o2g", row["O2_gross"], "percent a year", s, fmt=PCT1)
        if row.get("O2_net") is not None:
            R.put(f"{k}_o2n", row["O2_net"], "percent a year", s, fmt=PCT1)
        if row["area"] == "US":
            R.put(f"{k}_ior", row["D3_rate_first"], "percent a year", s, fmt="{:.2f}%")
            R.put(f"{k}_mich", row["D6_michigan_m0"], "percent (expected inflation)", s, fmt=PCT1)
            R.put(f"{k}_nasdaq", row["O4_nasdaq_pct"], "percent over 36 months", s, fmt="{:+.0f}%")
            R.put(f"{k}_houses", row["O4_houses_pct"], "percent over 36 months", s, fmt="{:+.0f}%")
        else:
            R.put(f"{k}_dfr", row["D3_deposit_rate_m0"], "percent a year", s, fmt="{:.2f}%")


def _c26_as_c18(c26: dict, c18: dict) -> dict:
    """C26's run in the shape ``deciders`` reads C18's (the described rows are the United States' and the euro
    area's, which the fill does not touch)."""
    return {"headline": c26["headline"], "episodes": c26["episodes"], "what_happened": c26["what_happened"],
            "two_thirds": {o: {d: v["filled"] for d, v in c26["two_thirds"][o].items()} for o in c26["two_thirds"]},
            "counted": c26["counted"], "coincidence": c26["coincidence"],
            "accommodation_apart": c26["accommodation_apart"], "described_us_euro": c18["described_us_euro"]}


def deciders_war(R: Reg) -> None:
    """C24 (C18's war-out run with the wars of 1946-1988 coded from UCDP/PRIO), read beside C18; and, as the text
    reads the filled prices, the same count on C26's run (the war-out run on the filled CPI), whose keys are the
    ``a5_war_*`` ones; C24's own stay under ``a5_u_war_*``."""
    r = load("C24-a5-deciders-war-coded")
    assert not r["void"], "C24's headline rerun did not reproduce C18"
    r26 = load("C26-a5-deciders-hko-fill")
    assert not r26["void"], "C26's unfilled CPI did not reproduce C15, C18 and C24"
    s = "code/deciders.py (card C24)"
    s26 = "code/gap5_fill.py (card C26)"
    R.cite("a5_war_threshold", 1000, "battle deaths in a year", "the study's card C24-a5-deciders-war-coded",
           "parameters, war_threshold_battle_deaths", fmt="{:,.0f}")
    R.put("a5_war_pre89_list", r26["list_episodes_before_1989"], "episodes", s26)
    R.put("a5_war_pre89_coded", r26["list_episodes_before_1989_war_coded"], "episodes", s26)
    assert r26["list_episodes_before_1989"] == r["list_episodes_before_1989"]
    R.put("a5_u_war_pre89_coded", len(r["list_episodes_before_1989_war_coded"]), "episodes", s)
    for reading in ("design", "m0"):
        o, o26 = r["episodes_out"][reading], r26["episodes_out"][reading]
        R.put(f"a5_war_pre89_{reading}", o26["before_1989"], "episodes", s26)
        R.put(f"a5_war_out_{reading}", o26["out"], "episodes", s26)
        R.put(f"a5_u_war_pre89_{reading}", o["before_1989"], "episodes", s)
        R.put(f"a5_u_war_out_{reading}", o["out"], "episodes", s)
    R.put("a5_war_cells_differ", r26["war_out_cells_differing_from_filled_headline"], "verdict cells of 12", s26)
    R.put("a5_u_war_cells_differ", r["cells_differing_from_headline"], "verdict cells of 12", s)


def fill_a4(R: Reg) -> None:
    """C25 (C02's model with the annual CPI gaps filled from the World Bank's inflation database), read beside
    C02, and on C22's grid beside C22."""
    r = load("C25-a4-base-hko-fill")
    assert not r["void"], "C25's unfilled panel did not reproduce C02 and C22"
    s = "code/gap5_fill.py (card C25)"
    PP = "points of inflation per point of money growth"
    for tag, key in (("C02_grid", "fill_c02"), ("C22_grid", "fill_c22")):
        x = r[tag]
        for state, k in (("filled", key), ("unfilled", f"{key}_before")):
            f = x[state]
            R.put(f"{k}_n", f["windows"], "decade windows", s)
            R.put(f"{k}_moneys", f["moneys"], "moneys", s)
            for suffix, v in (("beta", f["beta"]), ("lo", f["lo"]), ("hi", f["hi"])):
                R.put(f"{k}_{suffix}", v, PP, s, fmt="{:.2f}")
            for way in ("pi", "mu"):
                p = f[f"line_{way}"]
                for side in ("below", "above"):
                    R.put(f"{k}_{way}_{side}", p[f"beta_{side}"], "points per point", s, fmt="{:.2f}")
                    R.put(f"{k}_{way}_{side}_lo", p[f"beta_{side}_lo"], "points per point", s, fmt="{:.2f}")
                    R.put(f"{k}_{way}_{side}_hi", p[f"beta_{side}_hi"], "points per point", s, fmt="{:.2f}")
                    R.put(f"{k}_{way}_{side}_n", p[f"windows_{side}"], "decade windows", s)
            ho = f["held_out"]
            R.put(f"{k}_ho_beta", ho["beta"], "points per point", s, fmt="{:.2f}")
            R.put(f"{k}_ho_lo", ho["lo"], "points per point", s, fmt="{:.2f}")
            R.put(f"{k}_ho_hi", ho["hi"], "points per point", s, fmt="{:.2f}")
            R.put(f"{k}_folds_differing", f["folds_differing"], "folds", s)
        R.put(f"{key}_added", x["n_added"], "decade windows", s)
        R.put(f"{key}_moneys_added", len(x["moneys_added"]), "moneys", s)
    R.put("fill_a4_economies_filled", r["fill"]["economies_filled"], "economies", s)
    R.put("fill_a4_economies_refused", len(r["fill"]["economies_refused_by_the_guard"]), "economies", s)
    R.put("fill_a4_years_added", r["fill"]["years_added_total"], "economy-years", s)


def fill_deciders(R: Reg) -> None:
    """C26 (C24's run with the monthly CPI gaps filled), read beside C18 and C24."""
    r = load("C26-a5-deciders-hko-fill")
    assert not r["void"], "C26's unfilled CPI did not reproduce C15, C18 and C24"
    s = "code/gap5_fill.py (card C26)"
    R.put("fill_a5_months", r["fill"]["months_added"], "economy-months", s)
    R.put("fill_a5_economies", len(r["fill"]["by_economy"]), "economies", s)
    R.put("fill_a5_economies_refused", len(r["fill"]["refused_by_the_guard"]), "economies", s)
    R.put("fill_a5_cells_differ", r["cells_differing_from_c18"], "verdict cells of 12", s)
    R.put("fill_a5_war_out_cells_differ", r["war_out_cells_differing_from_c24"], "verdict cells of 12", s)
    for reading in ("design", "m0"):
        mv = r["tested_set_movement"][reading]
        R.put(f"fill_a5_tested_{reading}_before", mv["n_unfilled"], "episodes", s)
        R.put(f"fill_a5_tested_{reading}", mv["n_filled"], "episodes", s)
        R.put(f"fill_a5_enter_{reading}", len(mv["enter"]), "episodes", s)
        R.put(f"fill_a5_leave_{reading}", len(mv["leave"]), "episodes", s)


def fill_variants(R: Reg) -> None:
    """From C26's counted runs: the smoothing and the seam variants' cells beside the headline's (the long says
    which cell), and the count of the gross broad money / exchange rate cell over the counted runs."""
    r = load("C26-a5-deciders-hko-fill")
    s = "code/gap5_fill.py (card C26)"
    head = r["headline"]["combined"]

    def differing(name: str) -> list[str]:
        c = r["counted"][name]["combined"]
        return [f"{o} / {d}" for o in c for d in c[o]
                if c[o][d]["verdict"] != head[o][d]["verdict"] or c[o][d]["sign"] != head[o][d]["sign"]]
    for name, key in (("smoothing", "smooth"), ("seam episodes out", "seam")):
        cells = differing(name)
        assert cells == ["O2_gross / D1"], (name, cells)  # the long names this one cell
        R.put(f"a5_{key}_cells_differ", len(cells), "verdict cells of 12", s)
        R.put(f"a5_{key}_cells_same", 12 - len(cells), "verdict cells of 12", s)
    verdicts = [c["combined"]["O2_gross"]["D1"]["verdict"] for c in r["counted"].values()]
    R.put("a5_o2g_d1_nosep", sum(v == "does not separate" for v in verdicts), "counted runs", s)
    R.put("a5_o2g_d1_keep", sum(v == head["O2_gross"]["D1"]["verdict"] for v in verdicts), "counted runs", s)
    assert len(verdicts) == 29


def margins_filled(R: Reg) -> None:
    """The margin check re-measured on the filled panel (a diagnostic, not a card: ``gap5_margins_filled.py``), and
    the earlier margin check's numbers on the unfilled panel, cited from its dated note."""
    import re
    j = json.loads((K.STUDY / "results" / "diagnostics" / "gap5-margins-filled-2026-10-02.json").read_text())
    s = "code/gap5_margins_filled.py (a diagnostic, no card)"
    d = j["deciders"]
    R.put("margin_dec_cells", d["cells"], "verdict cells", s)
    R.put("margin_dec_weak", d["margin_at_or_below_U"], "verdict cells", s)
    R.put("margin_dec_flip", d["flip_when_only_narrow_U_change"], "verdict cells", s)
    row = next(r for r in d["rows"] if r[0] == "O2_gross / D1")
    R.put("margin_dec_o2g_d1_design", int(re.search(r"design: narrow (\d+),", row[10]).group(1)), "printings", s)
    for tag, name in (("base", "C25 on C02's grid"), ("c22", "C25 on C22's grid"), ("broad", "C27")):
        v = next(x for k, x in j["a4"].items() if k.startswith(name))
        R.put(f"margin_a4_{tag}_m", v["margin"], "windows removed", s)
        R.put(f"margin_a4_{tag}_unc", v["U"], "uncertain windows", s)
        R.put(f"margin_a4_{tag}_lost", v["lost"], "decade windows", s)
    note = "notes/gap5-margins-2026-10-02.md"
    for key, val, unit, loc in (
            ("margin_u_dec_weak", 11, "verdict cells", "In one paragraph"),
            ("margin_u_dec_flip", 2, "verdict cells", "In one paragraph"),
            ("margin_u_a4_base_m", 2, "windows removed", "A4 headline slopes, C02"),
            ("margin_u_a4_base_unc", 79, "uncertain windows", "A4 headline slopes, C02"),
            ("margin_u_a4_base_lost", 75, "decade windows", "A4 headline slopes, C02"),
            ("margin_u_a4_c22_m", 6, "windows removed", "A4 headline slopes, C22"),
            ("margin_u_a4_c22_unc", 68, "uncertain windows", "A4 headline slopes, C22"),
            ("margin_u_a4_broad_m", 1, "windows removed", "A4 headline slopes, C03"),
            ("margin_u_a4_broad_unc", 77, "uncertain windows", "A4 headline slopes, C03")):
        R.cite(key, val, unit, "the study's margin check of 2026-10-02 (" + note + ", the panel before the fill)", loc, fmt="{:.0f}")


def nicaragua(R: Reg) -> None:
    """One Nicaraguan window under each of the fill's two verdict changes (``gap5_nicaragua.py``, a diagnostic, no card):
    the filled runs read again without it. The filled reading stays the reading; the keys are the long's fragility sentence."""
    j = json.loads((K.STUDY / "results" / "diagnostics" / "gap5-nicaragua-2026-10-02.json").read_text())
    s = "code/gap5_nicaragua.py (a diagnostic, no card)"
    PP = "points of inflation per point of money growth"
    for tag, key, f3 in (("c22", "ni_c22", False), ("broad_ho", "ni_bho", True)):
        x = j[tag]
        R.put(f"{key}_mu", x["mu"], "percent a year", s, fmt=PCT0)
        R.put(f"{key}_pi", x["pi"], "percent a year", s, fmt=PCT0)
        assert x["cpi_source_y0"] == "annual" or tag == "broad_ho", x
        fm = "{:.3f}" if f3 else "{:.2f}"
        if tag == "c22":
            for suffix, v in (("beta", x["without"]["beta"]), ("lo", x["without"]["lo"]), ("hi", x["without"]["hi"])):
                R.put(f"{key}_wo_{suffix}", v, PP, s, fmt="{:.2f}")
            assert x["with"]["verdict"] == "one for one" and x["without"]["verdict"].startswith("partly")
        else:
            for suffix, v in (("beta", x["without"]["held_out_beta"]), ("lo", x["without"]["held_out_lo"]), ("hi", x["without"]["held_out_hi"])):
                R.put(f"{key}_wo_{suffix}", v, PP, s, fmt=fm if suffix != "beta" else "{:.2f}")
            R.put(f"{key}_with_beta", x["with"]["held_out_beta"], PP, s, fmt="{:.2f}")
            assert x["with"]["held_out_verdict"] == "one for one" and x["without"]["held_out_verdict"].startswith("partly")
    c = j["c02_without_nicaragua"]
    assert c["verdict"] == "one for one"
    for suffix, v in (("beta", c["beta"]), ("lo", c["lo"]), ("hi", c["hi"])):
        R.put(f"ni_c02_wo_{suffix}", v, PP, s, fmt="{:.2f}")


def earlier_lists(R: Reg) -> None:
    """The rule's first two versions, whose lists C18 reports beside, never counted (the grid check's G5)."""
    for card, key in (("C05-e-episodes", "c05"), ("C09-e-episodes-excess", "c09")):
        sm = load(card)["summary"]
        s = f"code/episodes.py (card {card.split('-')[0]})"
        R.put(f"e_{key}_episodes", sm["episodes"], "episodes", s)
        R.put(f"e_{key}_tested", sm["eligible"], "episodes", s)


def history(R: Reg) -> None:
    """The few numbers of the history section, cited as the series' design file records them (the dossier's
    genealogy table, bank/dossiers/FT-001-the-life-of-a-money.md, section 4, from its checked missions)."""
    for key, value, unit, source, locator, fmt in (
        ("hist_ming_face", 2, "percent of face value", "Richard von Glahn, Fountain of Fortune (1996)",
         "p. 74, n. 85 (1425: 'less than 2 percent of their face value')", PCT0),
        ("hist_restriction_premium", 45, "percent (premium of gold over notes)",
         "Pamfili M. Antipa, Journal of Economic History (2016)", "the premium in mid-1813 (doors' fact-check #1)",
         PCT0),
        ("hist_continental", 40, "dollars of bills per dollar of specie",
         "Farley Grubb, Journal of Economic History (2008)", "citing JCC v. 16, pp. 263-265 (18 March 1780)",
         "{:.0f}"),
        ("hist_hungary_hours", 15, "hours for prices to double", "Steve H. Hanke and Nicholas Krus (2012)",
         "World Hyperinflations, Hungary 1945-46", "{:.0f}"),
    ):
        R.cite(key, value, unit, source, locator, fmt=fmt)


def main() -> None:
    R = Reg()
    door(R)
    frame_list(R)
    tax(R)
    remittances(R)
    velocity(R)
    longrun(R)
    longrun_1870(R)
    longrun_2019(R)
    explore(R)
    longrun_dgp(R)
    c18, c26 = load("C18-a5-deciders-bare"), load("C26-a5-deciders-hko-fill")
    assert not c26["void"], "C26's unfilled CPI did not reproduce C15, C18 and C24"
    deciders(R, _c26_as_c18(c26, c18), "a5", "code/gap5_fill.py (card C26)")
    deciders(R, c18, "a5_u", "code/deciders.py (card C18)")
    deciders_war(R)
    fill_a4(R)
    fill_deciders(R)
    fill_variants(R)
    margins_filled(R)
    nicaragua(R)
    earlier_lists(R)
    history(R)
    registry_v15.add(R)  # map v15's new cards (C30-C33), round 2
    R.save()


if __name__ == "__main__":
    main()
