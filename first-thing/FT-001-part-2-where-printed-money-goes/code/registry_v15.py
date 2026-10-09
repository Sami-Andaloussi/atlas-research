"""The numbers of map v15's new cards (round 2, 2026-10-08): CS-B (C30), CS-C (C32), CS-E (C31) and CS-F's
correction (C33), written into the registry beside the reused cards' numbers (``registry.py`` calls :func:`add`).

Every estimate a claim rests on carries its labels (measure, period, population), its range, the size that matters
from its committed card (``matters``) and its reading, the card's own rule (P03) applied to the registered range;
a descriptive measurement carries its labels only. Nothing is recomputed: each value is the card's run as committed.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as K  # noqa: E402
import labels as LB  # noqa: E402  (the words of the labels the site prints: under 110 characters, STUDIES-WEB 14.3)

PP = "points of inflation per point of money growth"
SLOPE = "{:.2f}"
PCT0, PCT1 = "{:.0f}%", "{:.1f}%"
BN = "${:,.0f} billion"
TN = "${:.2f} trillion"
USD = "${:,.0f}"


def run(card: str) -> dict:
    return json.loads((K.RUNS / f"{card}.json").read_text())


def matters(card: str) -> dict:
    return yaml.safe_load((K.STUDY / "cards" / f"{card}.yaml").read_text())["matters"]


def card_reading(lo: float, hi: float, m: float) -> str:
    """The cards' P03 rule, as C30 and C31 wrote it before their runs: an effect only if the whole range lies beyond
    the size that matters."""
    if lo > m or hi < -m:
        return "effect"
    if -m <= lo and hi <= m:
        return "too small to matter"
    return "bounded"


def reading(lo: float, hi: float, m: float) -> str:
    """The engine's reading (``ft.readiness.reading_problems``, W18, F84), which the registry must hold: too small to
    matter if the range lies inside 0 +- m; an effect if it excludes 0 and is not wholly inside; bounded if it holds 0
    and reaches beyond m. Where the card's stricter rule reads otherwise (a range that excludes 0 but whose near end
    lies short of m), the card's reading is kept in the note and the text says what the range rules out."""
    if -m <= lo and hi <= m:
        return "too small to matter"
    if lo > 0 or hi < 0:
        return "effect"
    return "bounded"


def _est(R, key: str, est: dict, s: str, *, m: float | None, labels: dict, claim_type: str,
         run_reading: str | None = None, mkey: str | None = None, b: str = "gap", lo: str = "lo",
         hi: str = "hi") -> None:
    """The estimate under its card's matters key (``mkey``: the engine reads a key's size that matters from its
    card by name), its range and half-width under ``key``'s short prefix."""
    extra = {}
    if m is not None:
        cr = card_reading(est[lo], est[hi], m)
        if run_reading is not None:
            assert cr == run_reading, f"{key}: the card's rule reads {cr} on the registered range, the run {run_reading}"
        rd = reading(est[lo], est[hi], m)
        extra = {"matters": m, "reading": rd}
        if rd != cr:
            extra["note"] = (f"the card's own rule (an effect only if the whole range lies beyond {m:g}) reads it "
                             f"{cr}: the range excludes 0 but its near end lies short of {m:g}")
    R.put(mkey or key, est[b], PP, s, fmt=SLOPE, low=est[lo], high=est[hi], null=0.0, claim_type=claim_type,
          **extra, **labels)
    R.put(f"{key}_lo", est[lo], PP, s, fmt=SLOPE)
    R.put(f"{key}_hi", est[hi], PP, s, fmt=SLOPE)
    R.put(f"{key}_half", (est[hi] - est[lo]) / 2, PP, s, fmt=SLOPE)


def cs_b(R) -> None:
    """C30: base against broad money on the same calm windows."""
    out = run("C30-cs-b-base-against-broad")
    r, s, mt = out["result"], "code/cs_b.py (card C30)", matters("C30-cs-b-base-against-broad")
    assert not r["void"]
    pop = LB.POP_B

    def block(prefix: str, b: dict, period: str, mkey: str | None, population: str = pop) -> None:
        lab = {"measure": LB.BSLOPE, "period": period, "population": population}
        _est(R, f"{prefix}_gap", b["gap"], s, m=mt[mkey] if mkey else None, labels=lab, claim_type="comparative",
             run_reading=b["reading"] if mkey else None, mkey=mkey)
        for leg in ("base", "broad"):
            sl = b[f"slope_{leg}"]
            R.put(f"{prefix}_{leg}", sl["b"], PP, s, fmt=SLOPE, measure=f"slope on {leg} money growth",
                  period=period, population=population)
            R.put(f"{prefix}_{leg}_lo", sl["lo"], PP, s, fmt=SLOPE)
            R.put(f"{prefix}_{leg}_hi", sl["hi"], PP, s, fmt=SLOPE)
            R.put(f"{prefix}_cor_{leg}", b[f"cor_{leg}"], "correlation", s, fmt=SLOPE)
        R.put(f"{prefix}_dcor", b["dcor"], "correlation", s, fmt=SLOPE)
        R.put(f"{prefix}_dcor_lo", b["gap_bootstrap"]["dcor_ci"][0], "correlation", s, fmt=SLOPE)
        R.put(f"{prefix}_dcor_hi", b["gap_bootstrap"]["dcor_ci"][1], "correlation", s, fmt=SLOPE)
        R.put(f"{prefix}_gap_boot_lo", b["gap_bootstrap"]["gap_ci"][0], PP, s, fmt=SLOPE)
        R.put(f"{prefix}_gap_boot_hi", b["gap_bootstrap"]["gap_ci"][1], PP, s, fmt=SLOPE)
        R.put(f"{prefix}_windows", b["windows"], "decade windows", s)
        R.put(f"{prefix}_moneys", b["moneys"], "moneys", s)
        R.put(f"{prefix}_clusters", b["clusters"], "clusters", s)

    c = r["calm"]
    block("csb", c, LB.P_B, "cs_b_gap")
    R.put("csb_share_from_1990", 100 * c["share_from_1990"], "percent of the windows", s, fmt=PCT0)
    R.put("csb_line", 12, "percent a year", s, fmt=PCT0)
    R.put("csb_common_windows", r["common_windows"], "decade windows", s)
    R.put("csb_common_moneys", r["common_moneys"], "moneys", s)
    R.put("csb_reliability_needed", r["attenuation"]["reliability_needed"], "share", s, fmt=SLOPE)
    ck = r["checks"]
    block("csb_from1990", ck["from_1990"], "ten-year windows starting 1990 or later", "cs_b_gap_from_1990")
    block("csb_to1990", ck["to_1990"], "ten-year windows starting before 1990", "cs_b_gap_to_1990")
    block("csb_to2000", ck["era_to_2000"], "windows ending 1970–2000", "cs_b_gap_era_to_2000")
    block("csb_from2008", ck["era_from_2008"], "windows ending 2008–2020", "cs_b_gap_era_from_2008")
    jst = ck["jst_1870_1950"]
    jpop = "JST's rich economies, narrow money (base, notes or M1 by country) against broad money"
    block("csb_jst", jst["all"], "ten-year windows 1870 to 1950", "cs_b_gap_jst", jpop)
    block("csb_jst_nowar", jst["without_world_war_windows"], "ten-year windows 1870 to 1950 without the world wars",
          None, jpop)
    w = r["windows_holding_2008"]
    R.put("csb_2008_common", w["common"], "decade windows", s)
    R.put("csb_2008_dropped", w["dropped_by_the_base_rule_alone"], "decade windows", s)


def cs_c(R) -> None:
    """C32: the door's balance-sheet items, purchases against deficits, the public's money, and the facts K2-K5 tell."""
    r, s = run("C32-cs-c-door-timeline")["result"], "code/cs_c.py (card C32)"
    assert r["reproduction"]["all_match"]
    lab = {"period": "", "population": "the United States"}
    names = {"base": "the monetary base", "reserves": "bank reserves", "currency": "currency in circulation",
             "assets": "the Fed's total assets", "treasuries": "the Fed's Treasury holdings",
             "mbs": "the Fed's mortgage-backed securities"}
    for name, key in (("W1", "w1"), ("W2", "w2")):
        w = r["windows"][name]
        per = " to ".join(datetime.strptime(m, "%Y-%m").strftime("%B %Y") for m in (w["start"], w["end"]))
        R.put(f"csc_{key}_start", w["start"], "date", s)
        R.put(f"csc_{key}_end", w["end"], "date", s)
        R.put(f"csc_{key}_months", w["months"], "months", s)
        for item, unit_key in (("base_added_bn", "base"), ("reserves_added_bn", "reserves"),
                               ("currency_added_bn", "currency"), ("walcl_added_bn", "assets"),
                               ("treasuries_added_bn", "treasuries"), ("mbs_added_bn", "mbs")):
            R.put(f"csc_{key}_{unit_key}_tn", w[item] / 1000, "dollars", s, fmt=TN,
                  measure=f"change in {names[unit_key]}",
                  period=per, population=lab["population"])
        R.put(f"csc_{key}_reserves_share", w["reserves_share_pct"], "percent of the base added", s, fmt=PCT0,
              measure="reserves added over base money added", period=per, population=lab["population"])
        R.put(f"csc_{key}_currency_share", w["currency_share_pct"], "percent of the base added", s, fmt=PCT0)
        R.put(f"csc_{key}_purchases_share", w["purchases_share_fiscal_years_pct"], "percent of the deficits", s,
              fmt=PCT0, measure="Treasuries the Fed added in the printing, over its fiscal years' deficits",
              period=f"fiscal years {w['deficits_fiscal_years']['years'][0]} to "
              f"{w['deficits_fiscal_years']['years'][-1]}", population="the US")
        R.put(f"csc_{key}_purchases_share_mw", w["purchases_share_months_weighted_pct"], "percent of the deficits", s,
              fmt=PCT0)
        R.put(f"csc_{key}_deficits_tn", w["deficits_fiscal_years"]["sum_bn"] / 1000, "dollars", s, fmt=TN)
        R.put(f"csc_{key}_m2_pace", w["m2_pace_pa"], "percent a year", s, fmt=PCT1,
              measure="M2's compound growth", period=per, population="the United States")
        R.put(f"csc_{key}_m2_pace_before", w["m2_pace_before_pa"], "percent a year", s, fmt=PCT1)
    R.put("csc_m2_before_months", r["windows"]["W1"]["m2_before_months"], "months", s)
    R.put("csc_w2_reverse_repo_tn", r["windows"]["W2"]["reverse_repo_added_bn"] / 1000, "dollars", s,
          fmt="${:.1f} trillion", measure="change in reverse repurchase agreements (H.4.1 total)",
          period=f"{r['windows']['W2']['start']} to {r['windows']['W2']['end']}",
          population="the Federal Reserve's balance sheet")
    f = r["facts"]
    R.put("csc_m2_feb_may_2020_tn", f["m2_feb_to_may_2020_bn"] / 1000, "dollars", s, fmt="${:.1f} trillion",
          measure="change in M2", period="February to May 2020", population="the United States")
    R.put("csc_m2_feb_may_2020_pct", f["m2_feb_to_may_2020_pct"], "percent", s, fmt=PCT0)
    for q in ("2020Q1", "2020Q2", "2020Q4", "2021Q4"):
        R.put(f"csc_m2v_{q.lower()}", f[f"m2v_{q}"], "times a year", s, fmt="{:.2f}",
              measure="velocity of M2 (FRED M2V: nominal GDP over M2)", period=q, population="the United States")
    R.put("csc_m2_growth_2021", f["m2_growth_2021_dec_dec_pct"], "percent", s, fmt=PCT1,
          measure="M2, December 2020 to December 2021", period="2021", population="the United States")
    R.put("csc_ngdp_growth_2021", f["ngdp_growth_2021_q4_q4_pct"], "percent", s, fmt=PCT0,
          measure="nominal GDP, 2020Q4 to 2021Q4", period="2021", population="the United States")
    for month, v in f["unrate"].items():
        R.put(f"csc_unrate_{month.replace('-', '_')}", v, "percent of the labour force", s, fmt=PCT1,
              measure="unemployment rate (FRED UNRATE)", period=month, population="the United States")
    R.put("csc_unrate_line", 8, "percent of the labour force", s, fmt=PCT0)  # the card's dating of 2009-12's slack
    a, b = f["unrate_above_8_from_to"]
    R.put("csc_unrate_above8_from", a, "date", s)
    R.put("csc_unrate_above8_to", b, "date", s)
    d = r["decomposition"]
    R.put("csc_decomp_max_gap", d["max_gap_bars_vs_actual"], "points of annualised inflation", s, fmt=PCT1)


def cs_f(R) -> None:
    """C33: the reclassified savings read against other deposits' own path; the per-household range."""
    out = run("C33-cs-f-reclassification")
    r, s = out["result"], "code/cs_f.py (card C33)"
    assert not r["void"] and r["reproduction"]["holds"]
    rc = r["reclassification"]
    lab = {"measure": "other deposits below their own path",
           "period": "2020 Q4, when the April change shows", "population": "US households' savings deposits"}
    R.put("csf_R_bn", rc["main"]["R_bn"], "dollars", s, fmt=BN, **lab)
    R.put("csf_R_2019_bn", rc["beside_2019"]["R_bn"], "billion dollars", s, fmt=BN)
    for q, v in rc["spread_each_surrounding_quarter_alone_bn"].items():
        R.put(f"csf_R_alone_{q.lower()}_bn", v, "billion dollars", s, fmt=BN)
    R.put("csf_cap_bn", rc["cap_rise_in_move_quarter_bn"], "billion dollars", s, fmt=BN)
    g = r["range"]
    hh = {"measure": "what inflation took from cash and checking deposits",
          "period": " to ".join(datetime.strptime(r["beside_2019_baseline"]["period"][k], "%Y-%m").strftime("%B %Y")
                                for k in ("first_loss_month", "last_month")),
          "population": "the average US household"}
    for k in ("lower", "upper"):
        R.put(f"csf_hh_{k}", g[k], "dollars", s, fmt=USD, **hh)
        R.put(f"csf_hh_{k}_const", g[f"{k}_constant"], "dollars of February 2020", s, fmt=USD)
    R.put("csf_total_lower_bn", g["detail"]["lower_total_bn"], "billion dollars", s, fmt=BN)
    R.put("csf_total_upper_bn", g["detail"]["upper_total_bn"], "billion dollars", s, fmt=BN)
    R.put("csf_range_ratio", g["detail"]["range_ratio"], "times", s, fmt="{:.2f}")
    b19 = r["beside_2019_baseline"]["per_household"]
    R.put("csf_hh_lower_2019base", b19["lower_current"], "dollars", s, fmt=USD)
    R.put("csf_h6_move_month", r["monthly_timing_h6"]["h6_move_month"]["month"], "date", s)
    R.put("csf_h6_m1_change_bn", r["monthly_timing_h6"]["h6_move_month"]["m1_change_bn"], "billion dollars", s, fmt=BN)


def cs_e(R) -> None:
    """C31: the 2020-21 money against 2022-23 inflation across economies; Q6 on 2007-09 money."""
    r, s = run("C31-cs-e-pandemic-cross-section")["result"], "code/cs_e.py (card C31)"
    mt = matters("C31-cs-e-pandemic-cross-section")
    per = LB.P_E
    calm = LB.CALM

    def est(key: str, b: dict, slope: str, boot: str, mkey: str, population: str, run_reading: str | None,
            period: str = per, measure: str = "broad money slope"):
        e = {"b": b[slope], "lo": b[boot]["lo"], "hi": b[boot]["hi"]}
        _est(R, key, e, s, m=mt[mkey], labels={"measure": measure, "period": period, "population": population},
             claim_type="comparative", run_reading=run_reading, mkey=mkey, b="b")
        R.put(f"{key}_n", b["n"], "economies", s)
        if "clusters" in b:
            R.put(f"{key}_clusters", b["clusters"], "clusters", s)

    m = r["main"]
    pop = LB.CALM_E
    est("cse", m, "huber", "huber_boot", "cs_e_broad_huber", pop, m["reading"])
    est("cse_ols", m, "ols", "ols_boot", "cs_e_broad_ols", pop, m["ols_reading"],
        measure="broad money slope (OLS)")
    nc = r["main_no_control"]
    est("cse_nocontrol", nc, "huber", "huber_boot", "cs_e_broad_huber_no_control", calm, nc["reading"])
    names = {"a_currency": ("cse_var_currency", "cs_e_var_currency"), "b_led": ("cse_var_led", "cs_e_var_led"),
             "c_momentum": ("cse_var_momentum", "cs_e_var_momentum"),
             "d_net_claims": ("cse_var_net_claims", "cs_e_var_net_claims"),
             "e_no_hard_pegs": ("cse_var_no_pegs", "cs_e_var_no_dollarised"),
             "f_annual": ("cse_var_annual", "cs_e_var_annual"), "g_all": ("cse_var_all", "cs_e_var_all")}
    for v, (key, mk) in names.items():
        b = r["variants"][v]
        est(key, b, "huber", "huber_boot", mk, pop if v != "g_all" else "every economy with the data",
            b["reading"], period=per if v != "b_led" else LB.P_E_LED)
    R.put("cse_entering", r["coverage"]["entering"], "economies", s)
    R.put("cse_main_set", len(r["main_set"]), "economies", s)
    R.put("cse_control_missing", len(r["control_missing"]), "economies", s)
    loo = r["leave_one_out"]
    R.put("cse_loo_moves", sum(bool(x["moves"]) for x in loo), "economies", s)
    R.put("cse_loo_lo_min", min(x["lo"] for x in loo), PP, s, fmt=SLOPE)
    R.put("cse_loo_lo_max", max(x["lo"] for x in loo), PP, s, fmt=SLOPE)
    R.put("cse_null_p", r["null"]["p_value_one_sided"], "share of permutations", s, fmt="{:.3f}")
    R.put("cse_null_false", 100 * r["null"]["false_confirmation_rate"], "percent of permutations", s, fmt=PCT1)
    R.put("cse_null_draws", r["null"]["draws"], "permutations", s)
    h = r["h_base_described"]
    e = {"b": h["huber"], "lo": h["huber_boot"]["lo"], "hi": h["huber_boot"]["hi"]}
    _est(R, "cse_base", e, s, m=None, b="b", claim_type="described variant",
         labels={"measure": "base money slope", "period": per,
                 "population": calm})
    R.put("cse_base_top5_share", 100 * h["base_growth"]["share_of_variance_top5"], "percent of the variance", s,
          fmt=PCT0)
    R.put("cse_broad_top5_share", 100 * r["broad_growth"]["share_of_variance_top5"], "percent of the variance", s,
          fmt=PCT0)
    R.put("cse_cor_broad", h["cor_broad"], "correlation", s, fmt=SLOPE)
    R.put("cse_cor_base", h["cor_base"], "correlation", s, fmt=SLOPE)
    q = r["q6"]["read"]
    est("cse_q6", q, "huber", "huber_boot", "cs_e_q6_broad_huber", "economies whose 2003-07 inflation averaged "
        "below 10% a year, with the 2007 energy-import share", q["reading"],
        period="broad money December 2007 to December 2009; inflation December 2009 to December 2011")
    R.put("cse_q6_null_met", 100 * r["q6"]["null"]["prediction_met_under_null"], "percent of permutations", s,
          fmt=PCT1)
    R.cite("cse_bis_beta", 0.29, PP, "Borio, Hofmann & Zakrajsek (2023), BIS Bulletin 67",
           "p. 4, Graph 3 panel A (30 economies; excess broad money Q4 2019 to Q4 2020)", fmt=SLOPE)


def k3_cases(R) -> None:
    """K3 beyond one country (the grid check of 2026-10-08, J): numbers cited from the harvest of 2026-10-07."""
    R.cite("boj_base_2012", 138, "yen", "Bank of Japan, 4 April 2013", "p. 1, footnote 1",
           fmt="{:.0f} trillion yen")
    R.cite("boj_base_2014", 270, "yen", "Bank of Japan, 4 April 2013", "p. 1, footnote 1",
           fmt="{:.0f} trillion yen")
    R.cite("snb_assets_gdp", 87, "percent of GDP", "BIS Quarterly Review, March 2015",
           "overview, the paragraph on Swiss tensions", fmt=PCT0)
    R.cite("uk_cpi_2011_09", 5.2, "percent a year", "Bank of England, Inflation Report, November 2011; ONS D7G7",
           "p. 33, section 4.1; the series' September 2011 row", fmt=PCT1)
    R.cite("boe_apf_held_2011", 200, "pounds", "Bank of England, Inflation Report, November 2011", "p. 10",
           fmt="£{:.0f} billion")
    R.cite("boe_apf_2011", 275, "pounds", "Bank of England, Inflation Report, November 2011", "p. 5",
           fmt="£{:.0f} billion")


def door_scope(R) -> None:
    """The door's scope (Sami's remark through the engine, 2026-10-09: the two printings are not the only ones in
    American history). A descriptive measure, testing nothing: the growth of central-bank money (FRED BOGMBASE,
    vintage 2026-09-30, the one `C32` read) over each printing's window as `C32` stored it, against the largest growth
    over a window of the same length ending before the first printing began, since the series starts in 1959. The
    Second World War's balance sheet is cited from Judson and Weiss (2026)."""
    b = K.fred_monthly("BOGMBASE")
    w = run("C32-cs-c-door-timeline")["result"]["windows"]
    s = "FRED BOGMBASE (vintage 2026-09-30); the windows of C32's run; First Thing calculation"
    for key, win in (("w1", w["W1"]), ("w2", w["W2"])):
        start, end, n = pd.Period(win["start"], "M"), pd.Period(win["end"], "M"), int(win["months"])
        assert abs((b[end] - b[start]) - win["base_added_bn"]) < 0.5, f"{key}: BOGMBASE does not match C32's window"
        R.put(f"csc_{key}_base_growth", (b[end] / b[start] - 1) * 100, "percent", s, fmt=PCT0)
        pre = b[:pd.Period(w["W1"]["start"], "M")]
        grow = (pre / pre.shift(n) - 1).dropna() * 100
        R.put(f"csc_pre2008_max_growth_{n}m", float(grow.max()), "percent", s, fmt=PCT0)
    R.put("csc_base_first_month", int(b.index.min().year), "year", s, fmt="{}")
    jw = "Judson and Weiss (2026), 'A Brief Illustrated History of the Federal Reserve's Balance Sheet', FEDS Notes"
    R.cite("fed_bs_ww2_gdp", 22, "percent of GDP", jw, "section 4, first paragraph", fmt=PCT0)
    R.cite("fed_bs_2014_gdp", 25, "percent of GDP", jw, "section 7", fmt=PCT0)


def add(R) -> None:
    k3_cases(R)
    door_scope(R)
    cs_b(R)
    cs_c(R)
    cs_e(R)
    cs_f(R)
