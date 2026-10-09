"""Part 1's now (cards C06 and C08): the dollar, the euro, stablecoins and bitcoin coded on M0's list of supports. Told: no
margin, no verdict, nothing ranked. From the study's folder::

    ../../toolkit/bin/ftpy code/now.py

The card's readings are N1-N4. Readings made in code, in the open:

P1. *The last year read* is each source's own last year over all monies (Garriga's, Chinn-Ito's, the Bank of
    Canada-Bank of England database's), never a year chosen per money; a money with no reading in that year reads
    "cannot be read", with the reason the reader gives.
P2. *A limit by rule for a euro member* is read on Garriga's cap alone (``limit_by_rule_cap_only``): IRR codes a member
    as class 1 with a euro anchor, which is the member's use of the euro, not a peg the member keeps. The euro read as
    the member's own money (M0's first reading for euro members) has no parity. The dollar's limit by rule is frame
    c's full reading (the cap, or a parity class), at the class of the last year IRR reads.
P3. *Habit* is read as frame c reads it: "no" if an H1 act of the acts list is dated, "yes" inside the chronologies'
    span (to its last year), else "cannot be read".
P4. *World demand*: the money's allocated-reserves series is in COFER's annual release (the world, G001), with its
    share of the allocated total in the last year both are printed.

C08 (and C09 on the build after M7 section 16, with V5; and C10, the default, with V3') reads C06's code unchanged, with frame g's build after G25 (``mapping.csv``) and its V1-V4; given
C06's path, ``main`` runs C06 as it ran, on C06's build (``variant-fixed-readings-only.csv``, identical to
``mapping.csv`` at 97f10368).
"""

from __future__ import annotations

import csv
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
STUDY = HERE.parent
ROOT = STUDY.parents[1]
DATA = ROOT / "data"
REC = DATA / "reconstructed"
CARD = STUDY / "cards" / "C06-now-coded.yaml"
CARD_V2 = STUDY / "cards" / "C08-now-coded-g25.yaml"
CARD_V3 = STUDY / "cards" / "C09-now-coded-g25-checked.yaml"
CARD_V4 = STUDY / "cards" / "C10-now-who-rule.yaml"
CARD_V5 = STUDY / "cards" / "C12-now-coded-g25b.yaml"
CARD_V6 = STUDY / "cards" / "C14-now-institution-m0.yaml"
FRAME_A_MEMBERS = REC / "ft001-a" / "members.csv"
COBHAM_FULL = re.compile(r"first year from 2012 is (\d{4})")
G = REC / "ft001-g"
MAPPING_C06 = G / "variant-fixed-readings-only.csv"
WHO_FILE = G / "coders" / "who-classes.csv"
MAPPING_C10 = G / "variant-after-section-16.csv"
M0_WHO = ("any holder", "verified customers only", "not settled")
sys.path.insert(0, str(ROOT / "bank" / "maps" / "FT-001" / "missions" / "code"))

CANNOT = "cannot be read"
COFER = DATA / "imf" / "cofer" / "2026-10-01" / "cofer-allocated-annual.xml"
LINES = ("redemption", "limit by rule", "limit by institution", "taken back")

REDEMPTION_USD = {
    "reading": "no",
    "acts": [
        {"date": "1933-03", "act": "R1, convertibility suspended",
         "source": "Bernanke and James, Table 2.1, row United States (frame a, ft001-a, frame-a/bernanke-james-chapter)"},
        {"date": "1971-08-16", "act": "the dollar's convertibility to gold suspended for foreign central banks",
         "source": "Federal Reserve Bulletin, September 1971, p. A 92, note to the exchange-rate table "
                   "(fraser/federal-reserve-bulletin-text-091971, frozen 2026-10-01)"}],
}
REDEMPTION_EUR = {"reading": "no", "acts": [], "note": "frame a's lists, which date every convertibility the study "
                  "reads, carry none for the euro, which entered in 1999"}

BITCOIN = {
    "source": "Casey and Vigna (2015), The Age of Cryptocurrency, Picador, read through Mnemosyne's search "
              "(public), passage library/bc2767ae04dc04bf",
    "lines": {
        "redemption": "no issuer",
        "limit by rule": "yes",
        "limit by institution": "no issuer",
        "taken back": "no issuer",
    },
    "why": "the release of coins is fixed by the protocol's schedule, halving every four years, to 21 million in all "
           "(the passage); there is no issuer to redeem, be supervised or take the coin back",
    "not_opened": "bitcoin.org (the white paper) is refused by the Guard and was not opened",
}


def read_csv(path: Path) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def last_year(table: dict[str, dict[int, object]]) -> int:
    return max(y for v in table.values() for y in v)


def euro_members(rows: list[dict]) -> list[tuple[str, int]]:
    """The euro's members from their entry, the ECB's list as frame k wrote it (``dollar-euro.csv``)."""
    return sorted((r["economy"], int(r["first"])) for r in rows if r["currency"] == "EUR" and r["source"] == "ECB")


def habit(acts_rows: list[dict], coverage_rows: list[dict], money: str) -> dict:
    """P3."""
    h1 = [r["entry_date"] for r in acts_rows if r["money"] == money and r["route"] == "H1"
          and r["headline"] == "yes" and r["status"] == "counted"]
    spans = [(int(r["first_year"]), int(r["last_year"])) for r in coverage_rows
             if r["money"] == money and r["act"].split()[:1] == ["H1"]]
    if h1:
        return {"reading": "no", "year": None, "acts": h1}
    if not spans:
        return {"reading": CANNOT, "year": None, "why": "no H1 coverage in the acts list"}
    return {"reading": "yes", "year": max(b for _, b in spans), "why": "no H1 act in the chronologies' span"}


def cofer(path: Path = COFER) -> dict[str, dict]:
    """P4: {currency: {'year', 'share_pct'}} for the world's allocated reserves, in US dollars."""
    text = path.read_text()
    values: dict[str, dict[int, float]] = defaultdict(dict)
    for head, body in re.findall(r"<Series ([^>]*)>(.*?)</Series>", text, re.S):
        attrs = dict(re.findall(r'(\w+)="([^"]*)"', head))
        if attrs.get("COUNTRY") != "G001" or attrs.get("TYPE_OF_TRANSFORMATION") != "NV_USD":
            continue
        cur = attrs.get("FXR_CURRENCY", "").removeprefix("CI_")
        for obs in re.findall(r"<Obs ([^/]*)/>", body):
            o = dict(re.findall(r'(\w+)="([^"]*)"', obs))
            try:
                values[cur][int(o["TIME_PERIOD"])] = float(o["OBS_VALUE"])
            except (KeyError, ValueError):
                continue
    out = {}
    total = values.get("T", {})
    for cur in ("USD", "EUR"):
        years = sorted(set(values.get(cur, {})) & set(total))
        if not years:
            out[cur] = {"reading": CANNOT}
            continue
        y = years[-1]
        out[cur] = {"reading": "yes", "year": y, "share_pct": 100 * values[cur][y] / total[y]}
    return out


def money_supports(P, money: str, years: dict[str, int], garriga: dict, ka: dict, irr: dict,
                   member: bool) -> dict:
    """The four counted supports at the last year each source reads, by frame c's reader (panel.supports)."""
    g = garriga.get(money, {}).get(years["garriga"], {})
    default = P.default_at(money, years["default"])
    cls = None
    if not member:
        cls, _ = P.class_at(irr.get(money), 2017)        # the class of 2016, the last year IRR reads
    s = P.supports(default, g.get("cuk_limlen"), cls, g.get("lvau_garriga"), ka.get(money, {}).get(years["ka"]))
    by_rule = s["limit_by_rule_cap_only"] if member else s["limit_by_rule"]
    return {"taken_back": {"reading": s["taken_back"], "year": years["default"], "default": default},
            "limit_by_rule": {"reading": by_rule, "year": years["garriga"], "cap": g.get("cuk_limlen"),
                              "irr_class_2016": cls},
            "limit_by_institution": {"reading": s["limit_by_institution"], "year": years["garriga"],
                                     "index": g.get("lvau_garriga")},
            "force": {"reading": s["force"], "year": years["ka"], "ka_open": ka.get(money, {}).get(years["ka"])}}


def stablecoins(rows: list[dict]) -> dict:
    """Frame g's launch codes per line, as built (no line filled)."""
    launch = [r for r in rows if r["phase"] == "launch"]
    per_line = {line: dict(Counter(r["code"] for r in launch if r["line"] == line)) for line in LINES}
    read = Counter(r["coin_id"] for r in launch if r["code"] in ("yes", "no"))
    coins = {r["coin_id"] for r in launch}
    return {"coins": len(coins), "coin_lines": len(launch), "per_line": per_line,
            "coins_by_lines_read": dict(sorted(Counter(read.get(c, 0) for c in coins).items()))}


WHO_CLASSES = (
    ("not settled", lambda w: w.startswith("not settled")),
    ("a restricted set of participants", lambda w: "restricted set" in w),
    ("holders with an account", lambda w: any(x in w for x in ("customer", "member", "client", "verified", "account"))),
    ("any holder", lambda w: any(x in w for x in ("any user", "any holder", "permissionless"))),
)

# C10's V3': a stated absence of an account or of custody is read before the account words
WHO_CLASSES_V2 = (
    WHO_CLASSES[0], WHO_CLASSES[1],
    ("any holder", lambda w: any(x in w for x in ("permissionless", "no account", "non-custodial"))),
    WHO_CLASSES[2], WHO_CLASSES[3],
)


def who_class(words: str, classes=WHO_CLASSES) -> str:
    """C08's V3 (C10's V3' with ``WHO_CLASSES_V2``): the first class whose words match, in the card's order; none
    matching is printed, never filled."""
    w = words.lower()
    for name, match in classes:
        if match(w):
            return name
    return "unclassified"


def stablecoins_v2(rows: list[dict], classes=WHO_CLASSES) -> dict:
    """C08's V1, V3 and V4 on one build of frame g."""
    out = stablecoins(rows)
    none = out["coins_by_lines_read"].get(0, 0)
    out["coins_none_share_pct"] = 100 * none / out["coins"]
    redeem = sorted((r["coin_id"], who_class(r["who"], classes)) for r in rows
                    if r["phase"] == "launch" and r["line"] == "redemption" and r["code"] == "yes")
    by: dict[str, list[str]] = defaultdict(list)
    for coin, c in redeem:
        by[c].append(coin)
    out["who_classes"] = {c: by[c] for c in dict.fromkeys(n for n, _ in classes) if by[c]}
    if by["unclassified"]:
        out["who_classes"]["unclassified"] = by["unclassified"]
    out["readings_say_restricted"] = sorted(r["coin_id"] for r in rows if r["phase"] == "launch"
                                            and r["line"] == "redemption" and r["code"] == "yes"
                                            and "the readings' words: a restricted set" in r.get("note", ""))
    out["late_prints"] = sorted([r["coin_id"], r["line"], r["phase"]] for r in rows
                                if "late print" in r.get("note", "").lower())
    return out


def who_m0(rows: list[dict], classes: dict[str, str]) -> dict[str, list[str]]:
    """C12's V3'': each redemption yes line's class from the readers' settled file, in M0's two classes (and not
    settled); a line with no class there is printed as unclassified."""
    out: dict[str, list[str]] = defaultdict(list)
    for r in rows:
        if r["phase"] == "launch" and r["line"] == "redemption" and r["code"] == "yes":
            c = classes.get(r["coin_id"], "unclassified")
            out[c if c in M0_WHO else "unclassified"].append(r["coin_id"])
    return {c: sorted(out[c]) for c in M0_WHO + ("unclassified",) if out[c]}


def run_v5() -> dict:
    """C12: C10 on the build after G25b, who in M0's classes, C10's build beside."""
    out = run_v2(WHO_CLASSES_V2)
    rows = read_csv(G / "mapping.csv")
    classes = {r["coin_id"]: r["class"] for r in read_csv(WHO_FILE)}
    out["stablecoins"]["who_m0"] = who_m0(rows, classes)
    out["stablecoins_after_section_16"] = stablecoins_v2(read_csv(MAPPING_C10), WHO_CLASSES_V2)
    return out


def cobham_full(money: str, path: Path = FRAME_A_MEMBERS) -> int | None:
    """Frame a's variant from Cobham's full categories (FIT, FCIT): the first year from 2012 a money is in them."""
    for r in read_csv(path):
        if r["panel"] == "4-from-2012-var-cobham-full" and r["code"] == money:
            m = COBHAM_FULL.search(r["reason"])
            return int(m.group(1)) if m else None
    return None


def institution_m0(money: str, index: float | None, year: int, targets: dict, cobham: int | None) -> dict:
    """C14: the limit by institution today by M0's text (claim2's reader, as C13), with Cobham's reading beside:
    the same line with a target counted from the first year Cobham's full categories hold the money."""
    import claim2
    target = claim2.target_at(money, year, targets)
    reading = claim2.institution_m0(index, target)
    cobham_target = "yes" if cobham is not None and cobham < year else target
    return {"reading": reading, "year": year, "index": index, "target": target,
            "reading_cobham": claim2.institution_m0(index, cobham_target), "cobham_first_year": cobham}


def run_v6() -> dict:
    """C14: C12 as it runs, the dollar's and the euro members' limit by institution re-read by M0's text."""
    import claim2
    out = run_v5()
    targets = claim2.targets()
    year = out["years"]["garriga"]
    d = out["dollar"]["supports"]["limit_by_institution"]
    out["dollar"]["supports"]["limit_by_institution_c12"] = dict(d)
    out["dollar"]["supports"]["limit_by_institution"] = institution_m0("USA", d["index"], year, targets,
                                                                       cobham_full("USA"))
    euro = out["euro"]
    euro["counts_c12"] = {"limit_by_institution": euro["counts"]["limit_by_institution"]}
    emu = cobham_full("EMU")
    for m, v in euro["per_member"].items():
        v["limit_by_institution_c12"] = dict(v["limit_by_institution"])
        v["limit_by_institution"] = institution_m0(m, v["limit_by_institution"]["index"], year, targets, emu)
    euro["counts"]["limit_by_institution"] = dict(Counter(v["limit_by_institution"]["reading"]
                                                          for v in euro["per_member"].values()))
    euro["counts"]["limit_by_institution_cobham"] = dict(Counter(v["limit_by_institution"]["reading_cobham"]
                                                                 for v in euro["per_member"].values()))
    return out


def kappas() -> dict:
    """C08's V2: each layer's kappa on its own coin-lines."""
    import frame_g_mapping as F
    c = G / "coders"
    out = {}
    layers = [("first", "g1", "g2"), ("issuer", "i1", "i2")]
    if (c / "i3" / "mapping.csv").exists():
        layers.append(("issuer_2", "i3", "i4"))
    for layer, a, b in layers:
        n, agreed, k = F.kappa(F.launch(F.read(c / a / "mapping.csv")), F.launch(F.read(c / b / "mapping.csv")))
        out[layer] = {"coin_lines": n, "agreed": agreed, "kappa": k}
    return out


def run(mapping: Path = MAPPING_C06) -> dict:
    import panel as P
    garriga, ka, irr = P.garriga(), P.ka_open(), P.irr_classes()
    years = {"garriga": last_year(garriga), "ka": last_year(ka), "default": last_year(P.default_classes())}
    acts_rows = read_csv(REC / "ft001-acts" / "series.csv")
    cov_rows = read_csv(REC / "ft001-acts" / "coverage.csv")
    reserves = cofer()
    dollar = {"supports": money_supports(P, "USA", years, garriga, ka, irr, member=False),
              "redemption": REDEMPTION_USD, "habit": habit(acts_rows, cov_rows, "USA"),
              "world_demand": reserves["USD"],
              "default_reason": ("the database has no row for the United States" if "USA" not in P.default_classes()
                                 else "")}
    members = euro_members(read_csv(REC / "ft001-k" / "dollar-euro.csv"))
    per_member = {m: {"entry": first, **money_supports(P, m, years, garriga, ka, irr, member=True),
                      "habit": habit(acts_rows, cov_rows, m)} for m, first in members}
    counts = {k: dict(Counter(v[k]["reading"] for v in per_member.values()))
              for k in ("taken_back", "limit_by_rule", "limit_by_institution", "force", "habit")}
    euro = {"members": len(members), "counts": counts, "per_member": per_member, "redemption": REDEMPTION_EUR,
            "world_demand": reserves["EUR"]}
    return {"years": years, "dollar": dollar, "euro": euro,
            "stablecoins": stablecoins(read_csv(mapping)), "bitcoin": BITCOIN}


def run_v2(classes=WHO_CLASSES) -> dict:
    out = run(G / "mapping.csv")
    out["stablecoins"] = stablecoins_v2(read_csv(G / "mapping.csv"), classes)
    out["stablecoins_fixed_readings_only"] = stablecoins_v2(read_csv(MAPPING_C06), classes)
    out["kappa"] = kappas()
    return out


def main(card: Path = CARD_V6) -> Path:
    """Runs C12 (the default: C10 on the build after G25b, who in M0's classes), C10 (C09 with V3'), C09 (C08's code on the build after M7 section 16) or, given C06's path,
    C06 as it ran. C08 ran C09's code on the build at daf87773 (its result, f12a2a7e, is in git)."""
    from ft import cards
    cards.require_locked(card)
    if card == CARD_V2:
        raise ValueError("C08 ran on frame g at daf87773; its result is in git, and the build has moved (C09)")
    if card == CARD:
        return cards.write_result(STUDY, card, run())
    if card == CARD_V6:
        return cards.write_result(STUDY, card, run_v6())
    if card == CARD_V5:
        return cards.write_result(STUDY, card, run_v5())
    if card in (CARD_V3, CARD_V4):
        raise ValueError("C09 and C10 ran on frame g at 8ace613e; their results are in git, and the build has moved (C12)")
    return cards.write_result(STUDY, card, run_v2(WHO_CLASSES_V2 if card == CARD_V4 else WHO_CLASSES))


if __name__ == "__main__":
    print(main())
