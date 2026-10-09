"""Tests for claim1.py on toy rows (card C04; M0 v4.2 section 6, claim 1). Nothing here builds the panel."""

import json

import pytest

import claim1 as c


class FakeReader:
    """The reader's interface on dictionaries: pi/d/reserves by (money, year), the rest by year."""

    end = 2020

    def __init__(self, pi=None, d=None, res=None, war=None, default="no"):
        self._pi, self._d, self._res, self._war, self._default = pi or {}, d or {}, res or {}, war or {}, default

    def pi(self, m, y):
        return self._pi.get((m, y))

    def d(self, m, y):
        return self._d.get((m, y))

    def reserves_change(self, m, y):
        return self._res.get((m, y))

    def split(self, m, y):
        return "not recorded"

    def default(self, m, y):
        return self._default

    def regime(self, m, y):
        return "parity"

    def war(self, m, y):
        return self._war.get((m, y), "no")


def test_classify_priority_and_windows():
    assert c.classify_break(2000, [1997], True) == c.AFTER
    assert c.classify_break(2000, [1999, 2002], True) == c.AFTER          # after beats before
    assert c.classify_break(2000, [2000, 2002], True) == c.SAME           # same year beats before
    assert c.classify_break(2000, [2003], True) == c.BEFORE
    assert c.classify_break(2000, [1996, 2004], True) == c.NO_ACT         # outside y-3..y+3 on both sides
    assert c.classify_break(2000, [], True) == c.NO_ACT


def test_cannot_be_read_past_coverage_and_without_onset():
    assert c.classify_break(2015, [], readable=False) == c.UNREAD         # a source stops before y+3: never "none"
    assert c.classify_break(2015, [2013], readable=False) == c.AFTER      # an act found is read whatever the coverage
    assert c.classify_break(None, [2013], readable=True) == c.UNREAD      # J3


def test_covers_merges_intervals_and_a_missing_code_covers_nothing():
    assert c.covers([(1800, 1959), (1960, 2024)], 1955, 1965)             # the two sources of T2 join at 1959/1960
    assert not c.covers([(1800, 1958), (1960, 2024)], 1955, 1965)
    assert not c.window_readable({"T2": [(1960, 2024)]}, ("T2", "L1"), 1990, 1995)   # no L1 row
    cov = c.build_coverage([{"money": "AAA", "act": "T2 external", "source": "Reinhart and Rogoff, Varieties of crises",
                             "first_year": "1800", "last_year": "1959"},
                            {"money": "AAA", "act": "L3-target", "source": "Hammond", "first_year": "1990",
                             "last_year": "2012"}])
    assert cov["AAA"]["by_code"] == {"T2": [(1800, 1959)]}                # L3-target is no headline coverage (J2)


def test_supports_state_r5():
    base = {"taken_back": "no", "limit_by_rule": "no", "limit_by_institution": "no", "force": "no"}
    assert c.supports_state(base) == "none"
    assert c.supports_state({**base, "force": "yes"}) == "one"
    assert c.supports_state({**base, "force": "yes", "taken_back": "yes"}) == "two or more"
    assert c.supports_state({**base, "force": "cannot be read"}) == c.CANNOT          # none yes, one unread: left out
    assert c.supports_state({**base, "force": "yes", "taken_back": "cannot be read"}) == "one"   # the yes counted


def test_at_risk_years_rule():
    pi = {1979: 9.9, 1980: 10.0, 1981: 4.0, 1982: 4.0, 1983: 4.0, 1984: 4.0, 1985: 4.0, 1986: 4.0, 1987: 4.0}
    # entry 1981, H 10, onset 1985: y in 1981..1984; pi(y-1) must be below 10 (1980's 10.0 is not)
    years, unread = c.at_risk_years(1981, 10, 1985, pi.get, end=2020, from_year=1970)
    assert years == [1982, 1983, 1984] and unread == 0
    # held spell: to entry + H - 1 and not past the common end
    years, _ = c.at_risk_years(1981, 10, None, pi.get, end=1985)
    assert years == [1982, 1983, 1984, 1985]
    # pi(y-1) unreadable: not at risk, counted apart; years before 1970 are out
    years, unread = c.at_risk_years(1968, 5, None, {1969: 3.0, 1971: 3.0}.get, end=2020)
    assert years == [1970, 1972] and unread == 1          # 1971's pi(1970) is unread; 1968-69 are before 1970


def test_exposure():
    assert c.exposure(2000, [2000], True) == c.EXPOSED
    assert c.exposure(2000, [2000, 1999], False) == c.EXPOSED             # an act in the year is read whatever the coverage
    assert c.exposure(2000, [1998], True) == c.NEITHER                     # none in the year, one in the three before
    assert c.exposure(2000, [1996, 2001], True) == c.UNEXPOSED
    assert c.exposure(2000, [], False) == c.UNREAD                         # past a source's coverage, never "unexposed"


def test_forward_outcome_and_censoring():
    assert c.forward_outcome(2000, 2002, 2010) == (c.ONSET, False)
    assert c.forward_outcome(2000, 2004, 2010) == (c.NONE, False)          # onset later than y+3
    assert c.forward_outcome(2000, None, 2010) == (c.NONE, False)
    assert c.forward_outcome(2008, None, 2010) == (c.CENSORED, False)      # 2011 passes the end
    assert c.forward_outcome(2008, 2009, 2010) == (c.CENSORED, True)       # R4 read literally: censored, onset seen said
    assert c.forward_outcome(2007, None, 2010) == (c.NONE, False)          # y+3 = the last observed year: complete


def test_bins_at_the_cut_points():
    assert [c.pi_bin(v) for v in (4.99, 5, 9.99, 10, None)] == ["below 5", "5 to under 10", "5 to under 10",
                                                                  "10 or more", c.CANNOT]
    assert [c.d_bin(v) for v in (4.9, 5, 15)] == ["below 5", "5 to under 15", "15 or more"]
    assert [c.bin_above(v, (0, 5), c.DPI_LEVELS) for v in (-1, 0, 0.1, 5, 5.1)] == [
        "at most 0", "at most 0", "over 0 to 5", "over 0 to 5", "over 5"]
    assert [c.bin_above(v, (0, 10), c.DD_LEVELS) for v in (0, 10, 10.5)] == ["at most 0", "over 0 to 10", "over 10"]
    assert [c.reserves_bin(v) for v in (-20, -19.9, 5, None)] == [c.FALL, c.NO_FALL, c.NO_FALL, c.CANNOT]


def cell(n, onsets, censored=0):
    return {**c.new_cell(), "trials": n + censored, "n": n, "onsets": onsets, "censored": censored}


def test_mantel_haenszel_by_hand_on_two_strata():
    cells = {"a": {c.EXPOSED: cell(10, 4), c.UNEXPOSED: cell(30, 6)},          # N = 40
             "b": {c.EXPOSED: cell(20, 2), c.UNEXPOSED: cell(20, 4)},          # N = 40
             "one side": {c.EXPOSED: cell(5, 5), c.UNEXPOSED: cell(0, 0)}}     # no unexposed: out
    num = 4 * 30 / 40 + 2 * 20 / 40                                            # 3.0 + 1.0
    den = 6 * 10 / 40 + 4 * 20 / 40                                            # 1.5 + 2.0
    mh = c.mantel_haenszel(cells)
    assert mh["risk_ratio"] == pytest.approx(num / den) and mh["strata_with_both_sides"] == 2
    assert c.mantel_haenszel({"x": {c.EXPOSED: cell(3, 1), c.UNEXPOSED: cell(3, 0)}})["risk_ratio"] is None
    assert "note" in c.mantel_haenszel({"x": {c.EXPOSED: cell(3, 1), c.UNEXPOSED: cell(0, 0)}})


def test_censored_trials_are_counted_but_outside_the_rate():
    cell_ = c.new_cell()
    for outcome, seen in ((c.ONSET, False), (c.NONE, False), (c.CENSORED, True), (c.CENSORED, False)):
        c.add_trial(cell_, outcome, seen)
    done = c.finish_cell(cell_)
    assert (done["trials"], done["n"], done["censored"], done["censored_onset_seen"]) == (4, 2, 2, 1)
    assert done["rate"] == 0.5


def test_strata_read_the_year_before_in_a_and_the_year_itself_in_b():
    pi = {("M", 1989): 3.0, ("M", 1990): 12.0, ("M", 1988): 1.0, ("M", 1987): 1.0}
    rd = FakeReader(pi=pi, res={("M", 1989): -30.0, ("M", 1990): 0.0})
    spell = {"money": "M", "route": "c2", "tercile": "2", "supports": "one"}
    a = c.trial_strata(spell, 1990, 1989, rd)
    b = c.trial_strata(spell, 1990, 1990, rd)
    assert a["pi"] == "below 5" and b["pi"] == "10 or more"
    assert a["reserves"] == c.FALL and b["reserves"] == c.NO_FALL
    assert a["dpi1"] == "over 0 to 5" and b["dpi1"] == "over 5"             # 3 - 1 = 2 against 12 - 3 = 9
    assert a["dpi3"] == c.CANNOT                                           # pi(1986) unread: a level of its own
    assert a["decade"] == b["decade"] == "1990s" and a["supports"] == "one" and a["d"] == c.CANNOT


def test_line_window_r1_and_year_before_values():
    rd = FakeReader(pi={("M", 1988): 7.0}, d={("M", 1988): 12.345}, war={("M", 1988): "yes"})   # the year before 1989
    acts = [{"code": "T2", "year": y, "date": str(y), "source": "s", "group": "g"} for y in (1986, 1987, 1989, 1992, 1993)]
    brk = {"money": "M", "crossing": "1992-05", "crossing_year": 1992, "onset": "1990-02", "onset_year": 1990,
           "onset_route": "pi"}
    spells = [{"entry": 1975, "route": "c1", "tercile": "1"}, {"entry": 1990, "route": "c2", "tercile": "3"},
              {"entry": 1991, "route": "c4", "tercile": "2"}]
    line = c.build_line(brk, spells, acts, rd)
    assert [a["date"] for a in line["acts"]] == ["1987", "1989", "1992"]    # 1990 - 3 = 1987 to the crossing; 1993 is after
    assert line["frame_c"] == {"entry": 1990, "route": "c2", "tercile": "3"}   # at or before the onset's year, the last
    assert line["acts"][1]["year_before"] == {"pi": 7.0, "d": 12.35, "reserves_12m_change": c.CANNOT,
                                              "market_split": "not recorded", "war": "yes"}
    assert c.frame_c_spell([{"entry": 1995, "route": "c1", "tercile": "1"}], 1990) == c.NO_SPELL


def frame_b_row(money, crossing, onset, status="counted", route="pi"):
    return {"money": money, "entry_date": crossing, "break_onset": onset, "onset_route": route, "status": status}


def frame_c_row(money, entry, outcome, onset="", supports="yes", pi_ok=True):
    return {"money": money, "entry_date": str(entry), "H": "10", "status": "counted", "outcome": outcome,
            "onset_date": onset, "route": "c2", "tercile": "1", "taken_back": supports, "limit_by_rule": "no",
            "limit_by_institution": "no", "force": "no"}


def act_row(money, code, year, source="Garriga (2025), x"):
    return {"money": money, "route": code, "headline": "yes", "status": "counted", "entry_date": str(year),
            "source": source}


def test_build_result_end_to_end_on_toy_rows():
    monies = {"AAA": 1, "BBB": 2}
    pi = {(m, y): 3.0 for m in monies for y in range(1960, 2021)}
    rd = FakeReader(pi=pi)
    fb = [frame_b_row("AAA", "1985-06", "1984-01"), frame_b_row("BBB", "1975", "cannot be read"),
          frame_b_row("AAA", "1965", "1964"), frame_b_row("CCC", "1990", "1989"),          # before 1970; no spell
          frame_b_row("AAA", "1999", "1998", status="apart")]
    fc = [frame_c_row("AAA", 1980, "broke", onset="1984-01"), frame_c_row("BBB", 1972, "held"),
          frame_c_row("AAA", 2000, "held", supports="cannot be read")]                    # left out (R5)
    acts = [act_row("AAA", "L1", 1983), act_row("AAA", "T2", 1980, "Bank of Canada-Bank of England"),
            act_row("BBB", "L3", 1990)]
    cov = [{"money": m, "act": code, "source": src, "first_year": "1946", "last_year": "2023", "note": ""}
           for m in monies for code, src in (("T2", "Bank of Canada-Bank of England"), ("L1", "Garriga (2025)"),
                                             ("L2", "Ilzetzki, Reinhart"), ("L3", "Garriga (2025)"),
                                             ("H1", "Ilzetzki, Reinhart"))]
    res = c.build_result(fb, fc, acts, cov, rd, 2020)
    assert res["breaks"] == 2 and [ln["money"] for ln in res["lines"]] == ["BBB", "AAA"]
    assert res["lines"][0]["onset"] == c.CANNOT and res["lines"][0]["frame_c"]["entry"] == 1972    # J3: by the crossing
    sh = res["shares"]["overall"]
    assert sh["n"] == 2 and sh[c.AFTER]["n"] == 1 and sh[c.UNREAD]["n"] == 1     # AAA: L1 1983 before onset 1984
    assert res["shares"]["without_T2"][c.AFTER]["n"] == 1 and res["shares"]["onset_unreadable"] == 1
    assert res["base_rate"]["spells_left_out_supports"] == 1
    assert res["sentence"] == ("strain and expected inflation are not closed; a ratio above 1 here cannot be read as "
                               "the effect of an act.")
    assert set(res["forward_table"]) == {"A", "B"} and "T2 alone" in res["forward_table"]["A"]
    text = json.dumps(res).lower()
    assert "margin" not in text and "verdict" not in text
    assert all(k not in res for k in ("verdict", "margin", "outcome"))


def test_base_rate_years_and_war_variant():
    cov = {"M": {"by_code": {k: [(1946, 2023)] for k in c.HEADLINE}, "by_group": {}}}
    acts = {"M": [{"code": "T2", "year": 1988, "date": "1988", "source": "s", "group": "g"}]}
    trials = [{"money": "M", "y": y, "entry": 1985, "onset_year": None, "last_observed": 2020, "war": w,
               "A": {v: "x" for v in c.VARIABLES}, "B": {v: "x" for v in c.VARIABLES}}
              for y, w in ((1989, "no"), (1990, "yes"), (1992, "no"))]
    br = c.base_rate(trials, acts, cov)
    assert br["overall"]["with_act"] == 2 and br["overall"]["years"] == 3          # 1989, 1990 have 1988 in y-3..y-1
    assert br["without_T2"]["with_act"] == 0 and br["without_T2"]["share"] == 0
    ft = c.forward_table(trials, acts, cov)["A"]
    assert ft["war years apart: a war year in y"]["unexposed"]["n"] == 0 and \
        ft["war years apart: a war year in y"]["exposed"]["n"] == 0                # 1990 is "neither": act in the 3 before
    assert ft["all trials"]["trials_left_out"][c.NEITHER] == 2 and ft["all trials"]["unexposed"]["n"] == 1


def test_source_labels_and_headline_acts():
    assert c.source_label("T2", "Bank of Canada-Bank of England Sovereign Default Database") .startswith("T2 | Bank")
    assert c.source_label("L1", "Garriga (2025) cbi") == "L1 | Garriga (2025)"
    rows = [act_row("A", "L2", 1990), {**act_row("A", "L2-var-class", 1991)}, {**act_row("A", "T2", 1992), "headline": "no"},
            {**act_row("A", "H1", 1993), "status": "apart"}]
    assert [a["code"] for a in c.headline_acts(rows)["A"]] == ["L2"]


# --- card C07 (R6-R12) -------------------------------------------------------------------------------------------

def test_t2_variant_replaces_the_headline_from_1960_only():
    rows = [act_row("A", "T2", 1955, "Reinhart-Rogoff, Varieties"), act_row("A", "T2", 1980),
            {**act_row("A", "T2-var-total", 1982), "headline": "no", "status": "apart"}, act_row("A", "L1", 1990)]
    assert [(a["code"], a["year"]) for a in c.headline_acts(rows)["A"]] == [("T2", 1955), ("T2", 1980), ("L1", 1990)]
    assert [(a["code"], a["year"]) for a in c.headline_acts(rows, "T2-var-total")["A"]] == [
        ("T2", 1955), ("T2", 1982), ("L1", 1990)]


def test_shared_breaks_of_one_month_count_once():
    b = lambda m, onset, shared: {"money": m, "onset": onset, "onset_year": int(onset[:4]), "shared": shared}  # noqa: E731
    breaks = [b("BEN", "1994-01", True), b("SEN", "1994-01", True), b("COG", "1993-12", True), b("ARG", "1994-01", False)]
    assert [x["money"] for x in c.shared_once(breaks)] == ["BEN", "COG", "ARG"]
    assert c.decision_key("SEN", True, 1994, "1994-01") == ("shared", "1994-01")
    assert c.decision_key("ARG", False, 1994, "1994-01") == ("ARG", 1994)


def test_cells_count_distinct_breaks_beside_trial_years():
    items = [(c.EXPOSED, c.ONSET, False, {"v": 1}, ("M", 2000), ("shared", "2000-01")),
             (c.EXPOSED, c.ONSET, False, {"v": 1}, ("M", 2000), ("shared", "2000-01")),
             (c.EXPOSED, c.ONSET, False, {"v": 1}, ("N", 2000), ("shared", "2000-01")),
             (c.UNEXPOSED, c.NONE, False, {"v": 1}, ("P", None), ("P", None))]
    cell = c.cells_by(items, lambda s: "all")["all"]
    e = c.finish_cell(cell[c.EXPOSED])
    assert (e["onsets"], e["distinct_breaks"], e["distinct_decisions"]) == (3, 2, 1)
    assert c.finish_cell(cell[c.UNEXPOSED])["distinct_breaks"] == 0


def test_share_table_gives_the_readable_share_and_the_mh_note_names_the_empty_side():
    t = c.share_table([c.AFTER, c.AFTER, c.NO_ACT, c.UNREAD])
    assert t["readable"] == 3 and t[c.AFTER]["share"] == 0.5 and t[c.AFTER]["share_of_readable"] == pytest.approx(2 / 3)
    note = c.mantel_haenszel({"x": {c.EXPOSED: cell(3, 0), c.UNEXPOSED: cell(3, 0)}})["note"]
    assert note.startswith("no onset on either side")


def test_the_line_shows_acts_after_the_crossing_marked():
    rd = FakeReader()
    acts = [{"code": "T2", "year": y, "date": str(y), "source": "s", "group": "g"} for y in (1990, 1993)]
    brk = {"money": "M", "crossing": "1991", "crossing_year": 1991, "onset": "1990-06", "onset_year": 1990,
           "onset_route": "pi"}
    line = c.build_line(brk, [], acts, rd, after_crossing=True)
    assert [(a["date"], a.get("after_the_crossing", False)) for a in line["acts"]] == [("1990", False), ("1993", True)]
    assert [a["date"] for a in c.build_line(brk, [], acts, rd)["acts"]] == ["1990"]


def test_t2_inside_a_running_default():
    class R(FakeReader):
        def default(self, m, y):
            return "yes" if y == 1985 else "no"
    rows = [act_row("A", "T2", 1986), act_row("A", "T2", 1990), act_row("A", "T2", 1950)]
    assert c.t2_inside_default(rows, R()) == {"t2_lines_from_1960": 2, "inside_a_running_default": 1}


def test_build_result_v2_end_to_end_on_toy_rows():
    monies = {"AAA": 1, "BBB": 2}
    rd = FakeReader(pi={(m, y): 3.0 for m in monies for y in range(1960, 2021)}, war={("AAA", 1982): "yes"})
    fb = [frame_b_row("AAA", "1985-06", "1984-01"), frame_b_row("BBB", "1975", "cannot be read")]
    fc = [frame_c_row("AAA", 1980, "broke", onset="1984-01"), frame_c_row("BBB", 1972, "held")]
    acts = [act_row("AAA", "L1", 1983), act_row("AAA", "T2", 1980, "Bank of Canada-Bank of England"),
            {**act_row("AAA", "T2-var-total", 1979, "Bank of Canada-Bank of England"), "headline": "no",
             "status": "apart"}]
    cov = [{"money": m, "act": code, "source": src, "first_year": "1946", "last_year": "2023", "note": ""}
           for m in monies for code, src in (("T2", "Bank of Canada-Bank of England"), ("L1", "Garriga (2025)"),
                                             ("L2", "Ilzetzki, Reinhart"), ("L3", "Garriga (2025)"),
                                             ("H1", "Ilzetzki, Reinhart"))]
    res = c.build_result_v2(fb, fc, acts, cov, rd, 2020)
    assert set(res["readings"]) == {"headline", "T2-var-total", "T2-var-private"}
    head = res["readings"]["headline"]
    assert head["shares_base_rate_population"]["breaks"] == 1                     # AAA's 1984 onset ends its spell
    ft = head["forward_table"]["A"]
    assert {"headline: no war year in y", "a war year in y", "all trials (C04's headline)"} <= set(ft)
    assert ft["a war year in y"]["exposed"]["trials"] + ft["a war year in y"]["unexposed"]["trials"] + \
        sum(ft["a war year in y"]["trials_left_out"].values()) == 1                # 1982 alone
    assert "by_act_source" not in res["readings"]["T2-var-total"]["shares"]
    assert "verdict" not in json.dumps(res).lower()


def test_c15_rereads_only_counted_lines_and_keeps_the_rest(monkeypatch):
    import claim2

    class Fake:
        def __init__(self):
            pass
    monkeypatch.setattr(claim2, "Inputs", Fake)
    monkeypatch.setattr(claim2, "reproduces", lambda rows, inp: [])
    monkeypatch.setattr(claim2, "reread", lambda rows, inp: [{**r, "limit_by_institution": "no"} for r in rows])
    rows = [{"status": "counted", "limit_by_institution": "cannot be read"}, {"status": "apart", "limit_by_institution": "x"}]
    out = c.m0_frame_c(rows)
    assert out[0]["limit_by_institution"] == "no" and out[1] == rows[1]


def test_c15_refuses_when_frame_c_is_not_reproduced(monkeypatch):
    import claim2
    monkeypatch.setattr(claim2, "Inputs", lambda: None)
    monkeypatch.setattr(claim2, "reproduces", lambda rows, inp: ["ABW 2002 force: yes != no"])
    with pytest.raises(ValueError):
        c.m0_frame_c([{"status": "counted"}])
