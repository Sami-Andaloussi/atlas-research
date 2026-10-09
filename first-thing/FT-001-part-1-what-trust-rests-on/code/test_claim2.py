"""Tests for claim2.py on toy spells (card C05; M0 v4.2 section 6)."""

import pytest

import claim2 as c


def spell(money, side, outcome, route="c2", tercile="1", default="yes", year="1980", war="0"):
    return {"money": money, "status": "counted", "entry_date": year, "outcome": outcome, "route": route,
            "tercile": tercile, "era": "fiat", "default_at_entry": default, "supports_count": side,
            "war_years_in_H": war}


def test_mh_difference_by_hand():
    rows = ([spell(f"A{i}", c.TWO, "held") for i in range(3)] + [spell("B0", c.TWO, "broke")]
            + [spell(f"C{i}", c.FEWER, "held") for i in range(1)] + [spell("D0", c.FEWER, "broke")]
            + [spell(f"E{i}", c.TWO, "held", route="c1") for i in range(2)])           # c1 has one side only: out
    d, n, both = c.mh_difference(c.strata(rows, "supports_count"))
    assert both == 1 and n == [2, 4]
    assert d == pytest.approx(100 * (3 / 4 - 1 / 2))


def test_two_strata_are_weighted():
    s = {("a",): [[1, 0], [1, 1]], ("b",): [[0, 0, 0, 0], [1, 0, 0, 0]]}
    w1, w2 = 2 * 2 / 4, 4 * 4 / 8
    expected = 100 * (w1 * (1 - 0.5) + w2 * (0.25 - 0)) / (w1 + w2)
    assert c.mh_difference(s)[0] == pytest.approx(expected)


def test_unread_default_and_unread_side_are_out_and_before_1970_is_out():
    rows = [spell("A", c.TWO, "held", default="cannot be read"), spell("B", "cannot be read", "held"),
            spell("C", c.TWO, "held", year="1969")]
    assert c.strata(c.counted(rows), "supports_count") == {}
    assert len(c.counted(rows)) == 2


def test_restored_is_not_held():
    assert c.held({"outcome": "broke and restored"}) == 0 and c.held({"outcome": "held"}) == 1


def test_verdicts():
    assert c.verdict(30, 5, 50, [25, 30]) == "confirmed"
    assert c.verdict(30, -1, 50, [25, 30]) == "we cannot conclude"
    assert c.verdict(-5, -20, 9, [25, 30]) == "refuted"
    assert c.verdict(30, 5, 50, [19, 30]) == "too thin"
    assert c.verdict(None, None, None, [0, 0]) == "too thin"


def test_the_claims_verdict():
    assert c.claim_verdict("too thin", "confirmed", "confirmed") == "we cannot conclude (too thin)"
    assert c.claim_verdict("confirmed", "confirmed", "refuted").startswith("we cannot conclude (the verdict turns")
    assert c.claim_verdict("confirmed", "confirmed", "confirmed") == "confirmed"
    assert c.claim_verdict("we cannot conclude", "refuted", "confirmed") == "we cannot conclude"


def test_bootstrap_draws_monies_whole_and_is_seeded():
    rows = [spell(f"M{i}", c.TWO if i % 2 else c.FEWER, "held" if i % 3 else "broke") for i in range(40)]
    rows += [dict(r, entry_date="1990") for r in rows[:10]]          # a second spell of ten monies
    a = c.bootstrap(rows, "supports_count", draws=200, seed=5)
    assert a == c.bootstrap(rows, "supports_count", draws=200, seed=5)
    assert a[0] <= c.mh_difference(c.strata(rows, "supports_count"))[0] <= a[1] and a[2] == 0


def test_war_in_h():
    assert c.war_in_h({"war_years_in_H": "2"}) and not c.war_in_h({"war_years_in_H": "0 (+3 unreadable)"})
    assert c.war_in_h({"war_years_in_H": "1 (+1 unreadable)"})


def test_cfa_members_are_frame_a_union_table():
    members = c.cfa_members()
    assert {"CIV", "SEN", "CMR", "GAB", "GNQ", "TCD"} <= members
    assert not members & {"FRA", "DMA"}


T = {"NZL": ("adopted", 1989), "FIN": ("unread", None), "PRY": ("no", None), "IND": ("unread from", 2015)}


def test_target_at_orders_the_announcement_before_the_entry_year():
    assert c.target_at("NZL", 1990, T) == "yes"
    assert c.target_at("NZL", 1989, T) == "cannot be read"          # same year: not ordered
    assert c.target_at("NZL", 1985, T) == "no"
    assert c.target_at("FIN", 1985, T) == "cannot be read"           # an exit whose dates are not read
    assert c.target_at("PRY", 2015, T) == "no"
    assert c.target_at("IND", 2014, T) == "no" and c.target_at("IND", 2015, T) == "cannot be read"   # G06
    assert c.target_at("ZZZ", 2000, T) == "no"                       # on neither list


def test_institution_m0_reads_both_arms():
    assert c.institution_m0(0.6, "no") == "yes"
    assert c.institution_m0(0.3, "yes") == "yes"
    assert c.institution_m0(None, "yes") == "yes"
    assert c.institution_m0(0.3, "no") == "no"
    assert c.institution_m0(0.3, "cannot be read") == "cannot be read"
    assert c.institution_m0(None, "no") == "cannot be read"
    assert c.institution_m0(0.45, "no", line=0.4) == "yes"


def test_count_is_panels():
    assert c.count(["yes", "yes", "no", "no"]) == c.TWO
    assert c.count(["yes", "no", "no", "no"]) == c.FEWER
    assert c.count(["yes", "cannot be read", "no", "no"]) == "cannot be read"
    assert c.count(["cannot be read", "no", "no", "no"]) == c.FEWER


def test_targets_read_from_frame_a():
    t = c.targets()
    assert t["NZL"] == ("adopted", 1989) and t["JPN"] == ("adopted", 2013)
    assert t["FIN"] == ("unread", None) and t["IND"] == ("unread from", 2015)
    assert t["PRY"] == ("adopted", 2011) and t["UGA"] == ("adopted by", 2011) and t["URY"] == ("unread", None)
    assert c.target_at("PRY", 2015, t) == "yes" and c.target_at("UGA", 2003, t) == "cannot be read"
    assert c.target_at("UGA", 2012, t) == "yes"
    assert {m for m, v in t.items() if v == ("adopted by", 2011)} == {"UGA", "ALB", "GEO", "MDA"}
    assert sum(v[0] == "adopted" for v in t.values()) == 33


def test_composition_counts_spells_in_strata_with_both_sides_by_default():
    rows = ([spell("A", c.TWO, "held"), spell("B", c.FEWER, "broke"), spell("C", c.TWO, "held", default="no"),
             spell("D", c.TWO, "held", route="c1")])
    assert c.composition(rows, "supports_count") == {"yes": [1, 1], "no": [0, 0]}
