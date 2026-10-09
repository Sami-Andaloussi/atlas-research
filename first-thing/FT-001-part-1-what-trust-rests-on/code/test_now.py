"""Tests for now.py on toy rows (card C06)."""

import now as n


def test_euro_members_are_the_ecb_rows():
    rows = [{"economy": "AUT", "first": "1999", "currency": "EUR", "source": "ECB"},
            {"economy": "AUT", "first": "1999", "currency": "EUR", "source": "IRR"},
            {"economy": "AND", "first": "2002", "currency": "EUR", "source": "session"},
            {"economy": "PAN", "first": "1946", "currency": "USD", "source": "IRR"}]
    assert n.euro_members(rows) == [("AUT", 1999)]


def test_habit_reads_an_act_then_the_span():
    acts = [{"money": "X", "route": "H1", "headline": "yes", "status": "counted", "entry_date": "2001"}]
    cov = [{"money": "X", "act": "H1", "first_year": "1946", "last_year": "2016"},
           {"money": "Y", "act": "H1", "first_year": "1946", "last_year": "2016"}]
    assert n.habit(acts, cov, "X")["reading"] == "no"
    assert n.habit(acts, cov, "Y") == {"reading": "yes", "year": 2016, "why": "no H1 act in the chronologies' span"}
    assert n.habit(acts, cov, "Z")["reading"] == n.CANNOT


def test_cofer_share_at_the_last_common_year(tmp_path):
    def series(cur, obs):
        o = "".join(f'<Obs TIME_PERIOD="{y}" OBS_VALUE="{v}"/>' for y, v in obs)
        return (f'<Series COUNTRY="G001" INDICATOR="AFXRA" FXR_CURRENCY="CI_{cur}" '
                f'TYPE_OF_TRANSFORMATION="NV_USD" FREQUENCY="A">{o}</Series>')
    xml = "<x>" + series("USD", [(2023, 60), (2024, 58)]) + series("EUR", [(2023, 20)]) + \
        series("T", [(2023, 100), (2024, 100)]) + \
        '<Series COUNTRY="G001" FXR_CURRENCY="CI_USD" TYPE_OF_TRANSFORMATION="SHARE"><Obs TIME_PERIOD="2025" OBS_VALUE="1"/></Series></x>'
    p = tmp_path / "c.xml"
    p.write_text(xml)
    out = n.cofer(p)
    assert out["USD"] == {"reading": "yes", "year": 2024, "share_pct": 58.0}
    assert out["EUR"]["year"] == 2023 and out["EUR"]["share_pct"] == 20.0


def test_stablecoins_counts_launch_only():
    rows = [{"coin_id": "A", "line": "redemption", "phase": "launch", "code": "yes"},
            {"coin_id": "A", "line": "taken back", "phase": "launch", "code": "cannot be read"},
            {"coin_id": "B", "line": "redemption", "phase": "launch", "code": "cannot be read"},
            {"coin_id": "A", "line": "redemption", "phase": "after change", "code": "no"}]
    out = n.stablecoins(rows)
    assert out["coins"] == 2 and out["coin_lines"] == 3
    assert out["per_line"]["redemption"] == {"yes": 1, "cannot be read": 1}
    assert out["coins_by_lines_read"] == {0: 1, 1: 1}


def test_who_class_takes_the_first_rule_in_the_card_order():
    assert n.who_class("not settled: any investor (a); verified customers (b)") == "not settled"
    assert n.who_class("a restricted set of participants, the primary market") == "a restricted set of participants"
    assert n.who_class("any Xfers verified user") == "holders with an account"
    assert n.who_class("holders of Kinesis currency (via a Kinesis Mint or KCX account)") == "holders with an account"
    assert n.who_class("any user, by smart contract") == "any holder"
    assert n.who_class("users (permissionless, on-chain)") == "any holder"
    assert n.who_class("the issuer's friends") == "unclassified"


def test_stablecoins_v2_share_classes_and_late_prints():
    rows = [{"coin_id": "A", "line": "redemption", "phase": "launch", "code": "yes", "who": "any holder", "note": ""},
            {"coin_id": "B", "line": "redemption", "phase": "launch", "code": "cannot be read", "who": "", "note": ""},
            {"coin_id": "C", "line": "redemption", "phase": "launch", "code": "cannot be read", "who": "", "note": ""},
            {"coin_id": "D", "line": "redemption", "phase": "launch", "code": "yes", "who": "verified Members",
             "note": "late print (S10)"}]
    out = n.stablecoins_v2(rows)
    assert out["coins_none_share_pct"] == 50.0
    assert out["who_classes"] == {"holders with an account": ["D"], "any holder": ["A"]}
    assert out["late_prints"] == [["D", "redemption", "launch"]]
    assert out["readings_say_restricted"] == []
    rows[0]["note"] = "the readings' words: a restricted set of participants"
    assert n.stablecoins_v2(rows)["readings_say_restricted"] == ["A"]


def test_who_class_v2_reads_a_stated_absence_of_an_account_first():
    words = "LUSD holders (any user; permissionless) | holders / users (no account; non-custodial protocol)"
    assert n.who_class(words) == "holders with an account"                  # C08's V3, as C09 ran it
    assert n.who_class(words, n.WHO_CLASSES_V2) == "any holder"             # C10's V3'
    assert n.who_class("any Xfers verified user", n.WHO_CLASSES_V2) == "holders with an account"
    assert n.who_class("not settled: any investor; verified", n.WHO_CLASSES_V2) == "not settled"


def test_who_m0_reads_the_settled_file_and_never_fills():
    rows = [{"coin_id": "A", "line": "redemption", "phase": "launch", "code": "yes"},
            {"coin_id": "B", "line": "redemption", "phase": "launch", "code": "yes"},
            {"coin_id": "C", "line": "redemption", "phase": "launch", "code": "no"}]
    out = n.who_m0(rows, {"A": "verified customers only", "C": "any holder"})
    assert out == {"verified customers only": ["A"], "unclassified": ["B"]}


def test_c14_institution_reads_both_arms_and_cobham_beside():
    import claim2
    t = {"USA": ("no", None)}
    r = n.institution_m0("USA", 0.391, 2023, t, 2012)
    assert r["reading"] == "no" and r["reading_cobham"] == "yes" and r["target"] == "no"
    assert n.institution_m0("DEU", 0.9, 2023, t, 2022)["reading"] == "yes"
    assert n.institution_m0("USA", None, 2023, t, None)["reading"] == claim2.institution_m0(None, "no")


def test_cobham_full_reads_frame_a():
    assert n.cobham_full("USA") == 2012 and n.cobham_full("EMU") == 2022 and n.cobham_full("ZZZ") is None
