"""The numbers registry: every number part 1 prints, written into ``results/numbers.json`` with its unit, origin and
as-of date (BLUEPRINT §5 d). From the cards' results (``results/runs/``: C05, C07, C11, C12, C13, C14, C15) and from the committed outputs
of the datasets whose protocols are their cards (``plan/e2-ft001.md``, Decisions, "Part 1's cards"): A3's premiums
(``ft001-a3``), A2's window (``ft001-a-window``, through ``window_a``'s own summaries), frame k's shown cells
(``ft001-k``) and frame g's mapping (``ft001-g``). Numbers the study cites (Antipa's agio, the mint price, bitcoin's
cap) are entered as cited, with their source and locator. Called by ``run.py`` after the cards; rerunning it on the
same files gives the same registry.
"""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STUDY = HERE.parent
ROOT = STUDY.parents[1]
REC = ROOT / "data" / "reconstructed"
RUNS = STUDY / "results" / "runs"
sys.path.insert(0, str(ROOT / "bank" / "maps" / "FT-001" / "missions" / "code"))

from ft import numbers  # noqa: E402

sys.path.insert(0, str(HERE))
import registry_v11  # noqa: E402
import sources_v11  # noqa: E402

AS_OF = "2026-10-02"  # the vintage of the committed builds part 1 reads

PCT0, PCT1, PTS1, X2, X3 = "{:.0f}%", "{:.1f}%", "{:+.1f}", "{:.2f}", "{:.3f}"


def load(card: str) -> dict:
    return json.loads((RUNS / f"{card}.json").read_text())["result"]


def read_csv(path: Path) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


class Reg:
    def __init__(self) -> None:
        self.reg = numbers.Registry.load(STUDY / "results" / "numbers.json")
        self.reg.entries.clear()

    def put(self, key: str, value, unit: str, script: str, fmt: str | None = None) -> None:
        self.reg.put(key, value, unit=unit, origin=numbers.computed(script), as_of=AS_OF, fmt=fmt)

    def cite(self, key: str, value, unit: str, source: str, locator: str, fmt: str | None = None) -> None:
        self.reg.put(key, value, unit=unit, origin=numbers.cited(source, locator), as_of=AS_OF, fmt=fmt)

    def save(self) -> None:
        self.reg.save()


ANTIPA = "Antipa (2016), Journal of Economic History 76(4)"


def door(R: Reg) -> None:
    R.reg.put("as_of", AS_OF, unit="date", origin=numbers.computed("code/registry.py (the builds' vintage)"),
              as_of=AS_OF, fmt="%-d %B %Y")
    R.cite("door_agio_1800", 3, "percent", ANTIPA, "p. 1062 ('on 6 January 1800 the agio increased to 3 percent')",
           PCT0)
    R.cite("door_agio_peak", 45, "percent", ANTIPA, "p. 1056 ('reached a peak of 45 percent mid-1813')", PCT0)
    R.cite("a3_mint_price", 3.89375, "pounds an ounce of standard gold", "M0 v4.2 section 7; A3 card section 2",
           "£3 17s 10½d", "£3 17s 10½d")
    R.cite("a3_consols_coupon", 3, "percent coupon", "A3 card section 4", "3% consols (Millennium M10)", PCT0)
    R.cite("a3_flat_price", 4.0, "pounds an ounce", "Tooke (1838) vol. 2 p. 379", "1803 and 1805-1809", "£4")
    # the Bank of England's own balance sheet beside the door (both grid checks of 2026-10-07): its coin and bullion
    # against its notes in circulation, read from the frozen Millennium workbook, sheet A23
    import a3 as _a3  # noqa: PLC0415  (the mission's reader of the frozen workbook)
    import xlsx  # noqa: PLC0415
    a23 = {int(r[0]): r for r in xlsx.rows(_a3.MILLENNIUM, "A23. Bank of England B'Sheet")
           if r and isinstance(r[0], (int, float)) and 1796 <= r[0] <= 1801}
    src = "code/registry.py (Bank of England, A millennium of macroeconomic data, sheet A23)"
    for y, r in a23.items():
        bullion, notes = r[6], r[8]  # 'Coin and bullion' (assets), 'Notes In circulation' (liabilities), pounds
        R.put(f"door_boe_bullion_{y}", bullion / 1e6, "million pounds", src, fmt="£{:.1f} million")
        R.put(f"door_boe_notes_{y}", notes / 1e6, "million pounds", src, fmt="£{:.1f} million")
        R.put(f"door_boe_cover_{y}", 100 * bullion / notes, "percent of notes in circulation", src, fmt=PCT0)
    # goods prices beside the gold price (the confirming check's N3): the workbook's CPI inflation, sheet A47
    a47 = {int(r[0]): r for r in xlsx.rows(_a3.MILLENNIUM, "A47. Wages and prices")
           if r and isinstance(r[0], (int, float)) and 1797 <= r[0] <= 1800}
    srcp = "code/registry.py (Bank of England, A millennium of macroeconomic data, sheet A47, CPI inflation)"
    for y, r in a47.items():
        R.put(f"door_cpi_infl_{y}", r[4], "percent a year", srcp, fmt="{:.0f}%")
    R.put("door_cpi_fall_1797", -a47[1797][4], "percent a year", srcp, fmt="{:.0f}%")


def a3(R: Reg) -> None:
    s = "code/registry.py (ft001-a3, A3 card FT-001-M4-A3-premiums.md)"
    rows = read_csv(REC / "ft001-a3" / "series.csv")
    res = [r for r in rows if r["case"] == "the Bank Restriction" and r["P"] not in ("", "nan")]
    low = min(res, key=lambda r: float(r["P"]))
    R.put("a3_restriction_p_low", 100 * float(low["P"]), "percent of gold value", s, PCT0)
    R.put("a3_restriction_premium_low", 100 * (1 / float(low["P"]) - 1), "percent premium on gold", s, PCT0)
    war = [float(r["lambda"]) for r in res if 1810 <= int(r["period"]) <= 1816]
    R.put("a3_restriction_lambda_low", min(war), "a year", s, X2)
    R.put("a3_restriction_lambda_high", max(war), "a year", s, X2)
    R.put("a3_restriction_wait_low", 1 / max(war), "years", s, "{:.0f}")
    R.put("a3_restriction_wait_high", 1 / min(war), "years", s, "{:.0f}")
    gb = [r for r in rows if r["case"] == "the greenbacks" and r["P"] not in ("", "nan")]
    lowg = min(gb, key=lambda r: float(r["P"]))
    R.put("a3_greenback_p_low", 100 * float(lowg["P"]), "percent of gold value", s, PCT0)
    by_year: dict[int, list[float]] = {}
    for r in gb:
        if r["lambda"] not in ("", "nan"):
            by_year.setdefault(int(r["period"][:4]), []).append(float(r["lambda"]))
    means = [sum(v) / len(v) for y, v in by_year.items() if 1863 <= y <= 1869]
    R.put("a3_greenback_lambda_1863_69_low", min(means), "a year", s, X2)
    R.put("a3_greenback_lambda_1863_69_high", max(means), "a year", s, X2)
    R.put("a3_greenback_wait_low", 1 / max(means), "years", s, "{:.0f}")
    R.put("a3_greenback_wait_high", 1 / min(means), "years", s, "{:.0f}")
    after = [r for r in gb if r["phase"] == "after the law"]
    R.put("a3_greenback_after_law_months", len(after), "months", s)
    R.put("a3_greenback_after_law_cannot", sum(r["reading"] == "cannot separate" for r in after), "months", s)
    sens = read_csv(REC / "ft001-a3" / "r-sensitivity.csv")
    by_r = {round(float(r["r"]), 4): int(r["q_at_least_1"]) for r in sens if r["case"] == "the greenbacks"}
    lo, hi = min(by_r), min(r for r, m in by_r.items() if m == len(after))
    R.put("a3_r_low", 100 * lo, "percent", s, PCT1)
    R.put("a3_r_high", 100 * hi, "percent", s, PCT0)
    R.put("a3_greenback_after_law_r_low", by_r[lo], "months", s)
    cons = read_csv(REC / "ft001-a3" / "variant-r-consols.csv")
    R.put("a3_greenback_after_law_consols",
          sum(r["phase"] == "after the law" and r["reading"] == "cannot separate" for r in cons), "months", s)
    chk = read_csv(REC / "ft001-a3" / "check-1914.csv")
    for m in ("GBR", "FRA", "ITA", "DEU"):
        lam = [float(r["lambda"]) for r in chk if r["money"] == m and 1915 <= int(r["year"]) <= 1920
               and r["status"] == "counted" and r["lambda"] not in ("", "nan", "inf")]
        R.put(f"a3_1914_{m.lower()}", sum(lam) / len(lam), "a year, mean 1915-1920", s, X2)


PANELS = {"1": "p1", "2": "p2", "3-down": "p3d", "3-up": "p3u", "4": "p4"}


def a2(R: Reg) -> None:
    import window_a as W
    s = "code/registry.py (ft001-a-window, window_a.describe and robustness_notes)"
    d = REC / "ft001-a-window"
    changes = read_csv(d / "changes.csv")
    lines = W.describe(changes, read_csv(d / "null-band.csv"), read_csv(d / "placebo-band.csv"))
    means = {(x["reading"], x["label"], x["name"]): x for x in W.description_lines(changes)}
    pat = re.compile(r"^headline panel (\S+) \(counted\): n = (\d+), with a gap (\d+), mean gap ([+-][\d.]+); "
                     r"null band under no effect \[([+-]?[\d.]+), ([+-]?[\d.]+)\]")
    found = set()
    for line in lines:
        m = pat.match(line)
        if not m or m.group(1) not in PANELS:
            continue
        k = PANELS[m.group(1)]
        found.add(k)
        R.put(f"a2_{k}_n", int(m.group(3)), "changes with a gap", s)
        mean = next(v["mean"] for (rd, lab, name), v in means.items()
                    if rd == "headline" and lab == m.group(1) and name == "counted")
        R.put(f"a2_{k}_mean", mean, "percentage points", s, "{:+.2f}")
        R.put(f"a2_{k}_band_lo", float(m.group(5)), "percentage points", s, "{:+.2f}")
        R.put(f"a2_{k}_band_hi", float(m.group(6)), "percentage points", s, "{:+.2f}")
        # the effect's range, read as what it excludes (P03; the grid check of 2026-10-08, 2-3): the band of
        # chance under no effect, moved to the observed gap
        R.put(f"a2_{k}_eff_lo", mean - float(m.group(6)), "percentage points", s, "{:+.1f}")
        R.put(f"a2_{k}_eff_hi", mean - float(m.group(5)), "percentage points", s, "{:+.1f}")
    assert found == set(PANELS.values()), found
    v4 = re.compile(r"^a4-later-or-transition-documents panel 4 \(counted\): n = (\d+), with a gap (\d+), "
                    r"mean gap ([+-][\d.]+);")
    hits = [m for m in map(v4.match, lines) if m]
    assert len(hits) == 1, len(hits)
    R.put("a2_p4v_n", int(hits[0].group(2)), "changes with a gap", s)
    R.put("a2_p4v_mean", float(hits[0].group(3)), "percentage points", s, "{:+.2f}")
    single = re.compile(r"headline panel 2 \(counted, n = (\d+)\).*; (\d+) of the \d+ lines rest on a single comparator")
    for line in W.robustness_notes(changes):
        m = single.search(line)
        if m:
            R.put("a2_p2_single", int(m.group(2)), "lines", s)


CLASSES = (("after an act", "after"), ("same year", "same"), ("before an act", "before"), ("no act", "none"),
           ("cannot be read", "unread"))


def claim1(R: Reg) -> None:
    """Claim 1 from card C15 (C07 with the limit by institution read by M0's text); C07's figures that move are
    printed beside, and C04's run stays in git."""
    r = load("C15-claim1-institution-m0")
    s = "code/claim1.py (card C15)"
    c7 = load("C07-claim1-dated-lines-v2")
    s7 = "code/claim1.py (card C07)"
    for reading, pre in (("headline", "c1_c07"), ("T2-var-total", "c1_c07_tot")):
        br = c7["readings"][reading]["base_rate"]["overall"]
        R.put(f"{pre}_base_readable_n", br["with_act"] + br["no_act"], "readable strained years", s7)
        R.put(f"{pre}_base_sr", 100 * br["share_of_readable"], "percent of the readable strained years", s7, PCT0)
    for reading in ("headline", "T2-var-total", "T2-var-private"):
        assert r["readings"][reading]["shares"] == c7["readings"][reading]["shares"], \
            "the text says no share of breaks moves"
    R.put("c1_breaks", r["breaks"], "breaks", s)
    R.cite("c1_break_line", 20, "percent a year", "M0 v4.2 section 3, frame b", "the line (Reinhart and Rogoff)", PCT0)
    R.cite("c1_onset_pi", 10, "percent a year", "M0 v4.2 section 3, frame b", "the onset's lower line", PCT0)
    R.cite("c1_onset_d", 15, "percent a year", "M0 v4.2 section 3, frame b", "the onset's depreciation line", PCT0)
    R.cite("c1_strain_debt", 90, "percent of GDP", "M0 v4.2 section 3, frame c", "the debt route", PCT0)
    R.cite("c1_strain_deficit", 3, "percent of GDP", "M0 v4.2 section 3, frame c", "the deficit route", PCT0)
    R.cite("c1_at_risk_pi", 10, "percent a year", "M0 v4.2 section 6 (claim 1)", "strained at-risk years", PCT0)
    R.cite("now_index_line", 0.5, "Garriga's index, 0 to 1", "M0 v4.2 section 2", "a limit by institution", "{:.1f}")
    R.put("c1_t2_lines", r["t2"]["t2_lines_from_1960"], "T2 lines from 1960", s)
    R.put("c1_t2_inside", r["t2"]["inside_a_running_default"], "T2 lines", s)
    R.put("c1_shared_breaks", r["breaks_of_shared_monies"], "breaks", s)
    R.put("c1_once_breaks", r["breaks_shared_once"], "breaks", s)
    for reading, pre in (("headline", "c1"), ("T2-var-total", "c1_tot"), ("T2-var-private", "c1_prv")):
        v = r["readings"][reading]
        sh = v["shares"]["overall"]
        for name, k in CLASSES:
            R.put(f"{pre}_{k}_n", sh[name]["n"], "breaks", s)
            if name != "cannot be read":
                R.put(f"{pre}_{k}_sr", 100 * sh[name]["share_of_readable"], "percent of the readable breaks", s,
                      PCT0)
        R.put(f"{pre}_readable_n", sh["readable"], "readable breaks", s)
        br = v["base_rate"]["overall"]
        R.put(f"{pre}_base_readable_n", br["with_act"] + br["no_act"], "readable strained years", s)
        R.put(f"{pre}_base_sr", 100 * v["base_rate"]["overall"]["share_of_readable"],
              "percent of the readable strained years", s, PCT0)
        R.put(f"{pre}_pop_after_n" if pre == "c1" else f"c1_pop_{pre[3:]}_after_n",
              v["shares_base_rate_population"]["overall"]["after an act"]["n"], "breaks", s)
    head = r["readings"]["headline"]
    R.put("c1_pop_breaks", head["shares_base_rate_population"]["breaks"], "breaks", s)
    R.put("c1_once_after_n", head["shares_shared_once"]["overall"]["after an act"]["n"], "breaks", s)
    nt = head["shares"]["without_T2"]
    R.put("c1_not2_after_n", nt["after an act"]["n"], "breaks", s)
    R.put("c1_not2_before_n", nt["before an act"]["n"], "breaks", s)
    R.put("c1_not2_base_share", 100 * head["base_rate"]["without_T2"]["share_of_readable"],
          "percent of the readable strained years", s, PCT0)
    fa = head["forward_table"]["A"]["headline: no war year in y"]
    R.put("c1_fwd_e_n", fa["exposed"]["n"], "years", s)
    R.put("c1_fwd_e_onsets", fa["exposed"]["onsets"], "years", s)
    R.put("c1_fwd_e_breaks", fa["exposed"]["distinct_breaks"], "breaks", s)
    R.put("c1_fwd_u_n", fa["unexposed"]["n"], "years", s)
    R.put("c1_fwd_u_onsets", fa["unexposed"]["onsets"], "years", s)
    R.put("c1_fwd_u_breaks", fa["unexposed"]["distinct_breaks"], "breaks", s)
    R.put("c1_fwd_a_strata", fa["joint"]["strata_with_both_sides"], "strata", s)
    fb = head["forward_table"]["B"]["headline: no war year in y"]["joint"]
    R.put("c1_fwd_b_strata", fb["strata_with_both_sides"], "strata", s)
    if fb["risk_ratio"] is not None:
        R.put("c1_fwd_b_ratio", fb["risk_ratio"], "risk ratio", s, X2)
    R.put("c1_fwd_b_e_onsets", fb["onsets_exposed_there"], "years", s)
    R.put("c1_fwd_b_u_onsets", fb["onsets_unexposed_there"], "years", s)
    ft = r["readings"]["T2-var-total"]["forward_table"]["A"]["headline: no war year in y"]
    assert ft["exposed"]["onsets"] == 0, "the text says no year of a new default was followed by a break"
    R.put("c1_fwd_tot_e_n", ft["exposed"]["n"], "years", s)
    R.put("c1_fwd_tot_u_n", ft["unexposed"]["n"], "years", s)
    R.put("c1_fwd_tot_u_onsets", ft["unexposed"]["onsets"], "years", s)


def claim2(R: Reg) -> None:
    r = load("C13-claim2-institution-m0")
    s = "code/claim2.py (card C13)"
    R.cite("c2_margin", 10, "points", "M0 v4.2 section 6 (claim 2)", "the margin", "{:.0f}")
    R.cite("c2_floor", 20, "spells a side", "M0 v4.2 section 6 (claim 2)", "the floor", "{:.0f}")
    R.cite("c2_interval_level", 90, "percent", "M0 v4.2 section 6 (claim 2)", "the bootstrap interval", PCT0)
    R.put("c2_lines", r["lines"], "spells", s)
    R.put("c2_monies", r["monies"], "monies", s)
    assert r["claim"] == "we cannot conclude (too thin)", "the text says the comparison is too thin"
    for name, k in (("head", "supports_count"), ("tb", "supports_count_without_taken_back"),
                    ("np", "supports_count_without_pegs")):
        h = r["readings"][k]
        R.put(f"c2_{name}_n_fewer", h["n_one_or_none"], "spells", s)
        R.put(f"c2_{name}_n_two", h["n_two_or_more"], "spells", s)
        R.put(f"c2_{name}_d", h["D_points"], "points", s, "{:+.0f}" if name == "head" else "{:.0f}")
        R.put(f"c2_{name}_lo", h["interval_90"][0], "points", s, "{:.0f}")
        R.put(f"c2_{name}_hi", h["interval_90"][1], "points", s, "{:.0f}")
        R.put(f"c2_{name}_mde", h["mde_points"], "points", s, "{:.0f}")
    assert r["readings"]["supports_count_without_taken_back"]["outcome"] == "we cannot conclude"
    assert r["readings"]["supports_count_without_pegs"]["outcome"] == "confirmed"
    for v, key in (("yes", "yes"), ("no", "no"), ("cannot be read", "unread")):
        R.put(f"c2_inst_{key}", r["institution_lines"][v], "spells", s)
        R.put(f"c2_c05_inst_{key}", r["institution_lines_frame_c"][v], "spells", s)
    assert r["institution_lines_frame_c"]["no"] == 0, "the text says frame c's coding never read the line no"
    x = r["cfa_out"]["supports_count_without_pegs"]
    R.put("c2_np_d_nocfa", x["D_points"], "points", s, "{:.0f}")
    R.put("c2_np_lo_nocfa", x["interval_90"][0], "points", s, "{:.0f}")
    R.put("c2_np_hi_nocfa", x["interval_90"][1], "points", s, "{:.0f}")
    m = re.match(r"(\d+) of (\d+)", r["variants_counted"]["supports_count_without_pegs"])
    R.put("c2_np_variants", int(m.group(1)), "variants", s)
    R.put("c2_variants_n", int(m.group(2)), "variants", s)
    import claim2
    sc = "code/claim2.py (C13's lines: composition)"
    comp = claim2.composition(claim2.m0_lines(), "supports_count")
    assert comp["no"] == [0, 0], "the text says every stratum of the headline with both sides is in default"
    comp = claim2.composition(claim2.m0_lines(), "supports_count_without_pegs")
    R.put("c2_np_fewer_in_default", comp["yes"][0], "spells", sc)
    # Frame c's first coding, kept beside (C05, C11)
    c5 = load("C05-claim2-supports")
    s5 = "code/claim2.py (card C05)"
    for name, k in (("head", "supports_count"), ("np", "supports_count_without_pegs")):
        h = c5["readings"][k]
        R.put(f"c2_c05_{name}_n_fewer", h["n_one_or_none"], "spells", s5)
        R.put(f"c2_c05_{name}_n_two", h["n_two_or_more"], "spells", s5)
        R.put(f"c2_c05_{name}_d", h["D_points"], "points", s5, "{:+.0f}" if name == "head" else "{:.0f}")
    q = load("C11-claim2-cfa-out")
    R.put("c2_c11_d", q["supports_count_without_pegs"]["D_points"], "points", "code/claim2.py (card C11)", "{:.0f}")
    R.put("c2_nocfa_monies", len(q["left_out_monies"]), "member states", "code/claim2.py (card C11)")


def claim3(R: Reg) -> None:
    s = "code/registry.py (ft001-k, shown.csv and shown-variants.csv)"
    R.cite("c3_line", 5, "percent a year (real deposit return below minus this)", "M0 v4.2 section 6 (claim 3)",
           "frame k's line", PCT0)

    def cell(rows, variant):
        return next(r for r in rows if r["variant"] == variant and r["stratum_kind"] == "all"
                    and r["measure"] == "m1c" and r["basis"] == "gross")
    head = cell(read_csv(REC / "ft001-k" / "shown.csv"), "headline")
    var = read_csv(REC / "ft001-k" / "shown-variants.csv")
    for key, row in (("c3", head), ("c3_line0", cell(var, "line-0")), ("c3_areaer", cell(var, "areaer"))):
        name = "c3" if key == "c3" else key
        R.put(f"{name}_open" + ("_n" if key == "c3" else ""), int(row["n_open"]), "entries", s)
        R.put(f"{name}_closed" + ("_n" if key == "c3" else ""), int(row["n_closed"]), "entries", s)


def claim4_and_now(R: Reg) -> None:
    r = load("C14-now-institution-m0")
    s = "code/now.py (card C14)"
    sc = r["stablecoins"]
    R.put("c4_coins", sc["coins"], "coins", s)
    R.put("c4_coin_lines", sc["coin_lines"], "coin-lines", s)
    tot = {"yes": 0, "no": 0, "cannot be read": 0}
    for line in sc["per_line"].values():
        for k, v in line.items():
            tot[k] += v
    R.put("c4_unread", tot["cannot be read"], "coin-lines", s)
    R.put("c4_yes", tot["yes"], "coin-lines", s)
    R.put("c4_no", tot["no"], "coin-lines", s)
    R.put("c4_coins_none", sc["coins_by_lines_read"]["0"], "coins", s)
    R.put("c4_coins_none_pct", sc["coins_none_share_pct"], "percent of coins", s, PCT0)
    R.put("c4_coins_read", sc["coins"] - sc["coins_by_lines_read"]["0"], "coins", s)
    v = r["stablecoins_fixed_readings_only"]
    R.put("c4_coins_none_before", v["coins_by_lines_read"]["0"], "coins", s)
    issuer = set()
    for layer in ("i1", "i3"):
        issuer |= {x["coin_id"] for x in read_csv(REC / "ft001-g" / "coders" / layer / "mapping.csv")}
    R.put("c4_issuer_coins", len(issuer), "coins", "code/registry.py (ft001-g, coders/i1 and i3)")
    R.put("c4_issuer_sought", len(issuer) + 1, "coins", "code/registry.py (the coins read, and Reserve, sought with no capture)")
    R.put("c4_redeem_yes", sc["per_line"]["redemption"].get("yes", 0), "coins", s)
    R.put("c4_kappa", r["kappa"]["first"]["kappa"], "Cohen's kappa", s, X2)
    R.put("c4_kappa_issuer", r["kappa"]["issuer"]["kappa"], "Cohen's kappa", s, X2)
    R.put("c4_kappa_issuer2", r["kappa"]["issuer_2"]["kappa"], "Cohen's kappa", s, X2)
    who = sc["who_m0"]
    R.put("c4_redeem_any", len(who.get("any holder", [])), "coins", s)
    R.put("c4_redeem_account", len(who.get("verified customers only", [])), "coins", s)
    R.put("c4_redeem_readings_restricted", len(sc["readings_say_restricted"]), "coins", s)
    R.put("c4_redeem_unsettled", len(who.get("not settled", [])), "coins", s)
    assert "unclassified" not in who, who
    sw = "code/registry.py (ft001-g, coders/who-classes.csv)"
    wide = ("anyone", "any user", "holder", "everyone", "a user")
    bare = [x["coin_id"] for x in read_csv(REC / "ft001-g" / "coders" / "who-classes.csv")
            if x["class"] == "any holder" and '"users"' in x["reason_w1"].lower()
            and not any(w in (x["reason_w1"] + x["reason_w2"]).lower() for w in wide)]
    R.put("c4_redeem_any_bare", len(bare), "coins", sw)
    words = sc["who_classes"]                       # C10's word rule, on the same build, kept beside
    R.put("c4_c10_any", len(words.get("any holder", [])), "coins", s)
    R.put("c4_c10_account", len(words.get("holders with an account", [])), "coins", s)
    R.put("c4_c10_unclassified", len(words.get("unclassified", [])), "coins", s)
    d, e = r["dollar"], r["euro"]
    R.put("now_usd_cap", d["supports"]["limit_by_rule"]["cap"], "Garriga's lending-limits component, 0 to 1", s, X3)
    li = d["supports"]["limit_by_institution"]
    R.put("now_usd_index", li["index"], "Garriga's index, 0 to 1", s, X3)
    assert (li["reading"], li["reading_cobham"]) == ("no", "yes"), "the text says no by the rules, yes on Cobham's"
    assert d["supports"]["limit_by_institution_c12"]["reading"] == "cannot be read", "the text gives C12's reading"
    R.put("now_usd_cobham_year", li["cobham_first_year"], "year (Cobham's full categories)", s, "{:.0f}")
    assert e["counts"]["limit_by_institution"] == {"yes": e["members"]}, "the text says yes for all members"
    R.put("now_usd_cofer", d["world_demand"]["share_pct"], "percent of allocated reserves", s, PCT0)
    R.put("now_eur_cofer", e["world_demand"]["share_pct"], "percent of allocated reserves", s, PCT0)
    R.reg.put("now_cofer_year", f"{d['world_demand']['year']}-12", unit="date", origin=numbers.computed(s),
              as_of=AS_OF, fmt="%Y")
    R.put("now_eur_members", e["members"], "members", s)
    tb = e["counts"]["taken_back"]
    R.put("now_eur_tb_yes", tb.get("yes", 0), "members", s)
    R.put("now_eur_tb_no", tb.get("no", 0), "members", s)
    R.put("now_eur_tb_unread", tb.get("cannot be read", 0), "members", s)
    R.put("now_eur_force_no", e["counts"]["force"].get("no", 0), "members", s)
    R.put("now_eur_force_unread", e["counts"]["force"].get("cannot be read", 0), "members", s)
    R.cite("now_btc_cap", 21, "million coins", "Casey and Vigna (2015), The Age of Cryptocurrency",
           "library passage bc2767ae04dc04bf", "{:.0f} million")


def main() -> Path:
    R = Reg()
    door(R)
    a3(R)
    a2(R)
    claim1(R)
    claim2(R)
    claim3(R)
    claim4_and_now(R)
    registry_v11.add(R)  # map v11's new cards (C16, C18, C19, C20), round 2
    sources_v11.add(R)  # map v11's cited numbers and those read off frozen data (the door, K1-K8)
    R.save()
    return R.reg.path


if __name__ == "__main__":
    print(main())
