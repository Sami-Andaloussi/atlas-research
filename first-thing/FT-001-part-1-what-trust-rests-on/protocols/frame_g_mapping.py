"""FT-001 M7, frame g: the settled mapping (``mapping.csv``) from the two coders and the session's settlements.

Section 3: two coders apart (``coders/g1``, ``coders/g2``), κ on coin-lines, disagreements settled by M0's text, never by
the coin's fate (``coders/settlements.csv``, one row per settled coin-line, each with its rule S1-S8 of section 10).
This script adds nothing of its own (``series.csv`` restates the launch codes per coin, with the count of lines read):

- a launch coin-line both coders coded alike is kept, with both coders' sources;
- a launch coin-line they coded apart must have a settlement, or the script refuses;
- a settlement on an agreed line (S6: who may redeem) replaces it and is marked;
- after-change rows come from the settlements only (S7, S8): a printed change touches the lines it names, and the other
  lines stay in force from before.

κ is Cohen's, on the launch coin-lines, over the codes yes / no / cannot be read.

Section 14 (G25): a second layer, the issuers' own documents, coded by two more coders apart (``coders/i1``,
``coders/i2``, with a ``who`` column) on the coins the packet names, their disagreements settled in
``coders/issuer-settlements.csv`` (rule S11). :func:`issuer_layer` draws it as the first layer is drawn. :func:`merge`
sets it against the first layer (S11's second step): a first-layer *cannot be read* takes the issuer layer's code; two
codes read alike stand, sources joined; two read codes that differ need a row of ``coders/merge-settlements.csv``, or the
script refuses. Coins the issuer layer does not cover keep the first layer. The first layer is written beside as
``variant-fixed-readings-only.csv`` (and its series as ``variant-series-fixed-readings-only.csv``).

Run from the workshop's root:  toolkit/.venv/bin/python bank/maps/FT-001/missions/code/frame_g_mapping.py
"""

from __future__ import annotations

import csv
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
OUT = ROOT / "data" / "reconstructed" / "ft001-g"
LINES = ("redemption", "limit by rule", "limit by institution", "taken back")
CODES = ("yes", "no", "cannot be read")
FIELDS = ("coin_id", "line", "phase", "effective", "code", "who", "source", "locator", "settled", "note")


def read(path: Path) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def launch(rows: list[dict]) -> dict[tuple[str, str], dict]:
    """The launch coin-lines of one coder, refused if a line is doubled, unknown, or coded outside the three codes."""
    out: dict[tuple[str, str], dict] = {}
    for r in rows:
        if r["phase"] != "launch":
            continue
        key = (r["coin_id"], r["line"])
        if r["line"] not in LINES or r["code"] not in CODES:
            raise ValueError(f"unknown line or code: {key} {r['code']!r}")
        if key in out:
            raise ValueError(f"coin-line coded twice: {key}")
        out[key] = r
    return out


def kappa(a: dict, b: dict) -> tuple[int, int, float]:
    """(n, agreed, κ) on the coin-lines both coders coded. The two coders must have coded the same coin-lines."""
    if set(a) != set(b):
        raise ValueError(f"the coders coded different coin-lines: {sorted(set(a) ^ set(b))[:5]}")
    n = len(a)
    agreed = sum(a[k]["code"] == b[k]["code"] for k in a)
    ca, cb = Counter(a[k]["code"] for k in a), Counter(b[k]["code"] for k in b)
    po, pe = agreed / n, sum(ca[c] * cb[c] for c in CODES) / n**2
    return n, agreed, (po - pe) / (1 - pe) if pe < 1 else 1.0


def _join(x: str, y: str) -> str:
    x, y = (x or "").strip(), (y or "").strip()
    return x if x == y or not y else y if not x else f"{x} | {y}"


def mapping(g1: list[dict], g2: list[dict], settlements: list[dict]) -> list[dict]:
    a, b = launch(g1), launch(g2)
    kappa(a, b)
    settled_launch = {(s["coin_id"], s["line"]): s for s in settlements if s["phase"] == "launch"}
    apart = [k for k in a if a[k]["code"] != b[k]["code"] and k not in settled_launch]
    if apart:
        raise ValueError(f"disagreements with no settlement: {apart}")
    stray = [k for k in settled_launch if k not in a]
    if stray:
        raise ValueError(f"settlements on coin-lines no coder coded: {stray}")
    out = []
    for k in sorted(a):
        s = settled_launch.get(k)
        if s:
            out.append({"coin_id": k[0], "line": k[1], "phase": "launch", "effective": "launch", "code": s["code"],
                        "who": s["who"], "source": s["source"], "locator": s["locator"], "settled": s["rule"],
                        "note": s["note"]})
        else:
            out.append({"coin_id": k[0], "line": k[1], "phase": "launch", "effective": "launch", "code": a[k]["code"],
                        "who": "", "source": _join(a[k]["source"], b[k]["source"]),
                        "locator": _join(a[k]["locator"], b[k]["locator"]), "settled": "agreed", "note": ""})
    for s in settlements:
        if s["phase"] == "launch":
            continue
        if not s["phase"].startswith("after-change") or s["code"] not in CODES or s["line"] not in LINES:
            raise ValueError(f"bad after-change settlement: {s}")
        out.append({"coin_id": s["coin_id"], "line": s["line"], "phase": s["phase"], "effective": s["effective"],
                    "code": s["code"], "who": s["who"], "source": s["source"], "locator": s["locator"],
                    "settled": s["rule"], "note": s["note"]})
    return out


def issuer_layer(i1: list[dict], i2: list[dict], settlements: list[dict]) -> list[dict]:
    """Section 14: the issuer coders' layer, drawn as :func:`mapping` draws the first; ``who`` from the coders where they
    agree on it, else from the settlement (a redemption *yes* with two readings of who and no settlement is refused).
    S13 (section 16): a line either coder's note flags as a late print (S10) carries the flag in its note."""
    a, b = launch(i1), launch(i2)
    rows = mapping(i1, i2, settlements)
    for r in rows:
        k = (r["coin_id"], r["line"])
        if r["phase"] != "launch" or r["settled"] != "agreed":
            continue
        wa, wb = (a[k].get("who") or "").strip(), (b[k].get("who") or "").strip()
        if r["code"] == "yes" and r["line"] == "redemption" and wa and wb and wa != wb:
            r["who"] = f"{wa} | {wb}"
        else:
            r["who"] = wa or wb
        if any("late print" in (c[k].get("note") or "").lower() for c in (a, b)):
            r["note"] = _join(r["note"], "late print (S10)")
        r["settled"] = "issuer: agreed"
    for r in rows:
        if not r["settled"].startswith("issuer"):
            r["settled"] = f"issuer: {r['settled']}"
    return rows


def merge(first: list[dict], issuer: list[dict], merge_settlements: list[dict]) -> list[dict]:
    """S11's second step, line by line, for the coins the issuer layer covers; the others keep the first layer.
    S13 (section 16): where both layers read a line alike, who may redeem is the issuer's own words when the issuer
    layer has them, the reading's words kept in the note, and both layers' notes are kept; a line the first layer
    reads and the issuer layer cannot read keeps the first layer's code (a document that does not print a line does
    not undo a reading of it)."""
    first_l = {(r["coin_id"], r["line"]): r for r in first if r["phase"] == "launch"}
    iss_l = {(r["coin_id"], r["line"]): r for r in issuer if r["phase"] == "launch"}
    stray = [k for k in iss_l if k not in first_l]
    if stray:
        raise ValueError(f"issuer coin-lines not on the told list: {stray}")
    settled = {(s["coin_id"], s["line"]): s for s in merge_settlements}
    out = []
    for k in sorted(first_l):
        f, i = first_l[k], iss_l.get(k)
        if i is None:
            out.append(f)
            continue
        if f["code"] == "cannot be read":
            out.append({**i, "note": _join(i["note"], "first layer: cannot be read")})
        elif f["code"] == i["code"] and k not in settled:
            who, note = f["who"], _join(f["note"], i["note"])
            if i["who"]:
                who = i["who"]
                if f["who"] and f["who"] != i["who"]:
                    note = _join(note, f"the readings' words: {f['who']}")
            out.append({**f, "who": who, "source": _join(f["source"], i["source"]), "note": note,
                        "locator": _join(f["locator"], i["locator"]), "settled": _join(f["settled"], i["settled"])})
        elif i["code"] == "cannot be read" and k not in settled:
            out.append({**f, "note": _join(f["note"], "issuer layer: cannot be read")})
        else:
            s = settled.get(k)
            if s is None:
                raise ValueError(f"the two layers read {k} differently ({f['code']} / {i['code']}) and no merge settlement")
            if s["code"] not in CODES:
                raise ValueError(f"bad merge settlement: {s}")
            out.append({"coin_id": k[0], "line": k[1], "phase": "launch", "effective": "launch", "code": s["code"],
                        "who": s["who"], "source": s["source"], "locator": s["locator"], "settled": s["rule"],
                        "note": s["note"]})
    unused = [k for k in settled if k not in iss_l]
    if unused:
        raise ValueError(f"merge settlements on coin-lines the issuer layer did not code: {unused}")
    out += [r for r in first if r["phase"] != "launch"] + [r for r in issuer if r["phase"] != "launch"]
    return out


SERIES_FIELDS = ("period", "value", "unit", "source", "locator", "note", "uncertainty", "coin_id", "redemption", "who",
                 "limit by rule", "limit by institution", "taken back", "lines_yes", "after_change_rows")


def series(rows: list[dict]) -> list[dict]:
    """``series.csv``: one line per coin, its launch codes on the four lines, the number of lines **read** (yes or no)
    as the value, and how many after-change rows follow. Told: a count of lines read, never a score of the coin."""
    by_coin: dict[str, dict] = {}
    after: Counter = Counter()
    for r in rows:
        if r["phase"] != "launch":
            after[r["coin_id"]] += 1
            continue
        by_coin.setdefault(r["coin_id"], {})[r["line"]] = r
    out = []
    for coin in sorted(by_coin):
        lines = by_coin[coin]
        if set(lines) != set(LINES):
            raise ValueError(f"{coin}: launch lines {sorted(lines)} are not the four")
        codes = {l: lines[l]["code"] for l in LINES}
        out.append({"period": "launch", "value": sum(c != "cannot be read" for c in codes.values()),
                    "unit": "lines read at launch, of 4 (yes or no; the rest cannot be read)",
                    "source": "mapping.csv (two coders, settled)", "locator": coin, "note": "",
                    "uncertainty": "told; coders outcome-aware (section 3)", "coin_id": coin, **codes,
                    "who": lines["redemption"]["who"], "lines_yes": sum(c == "yes" for c in codes.values()),
                    "after_change_rows": after[coin]})
    return out


def write(path: Path, fields, rows: list[dict]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def main() -> None:
    c = OUT / "coders"
    g1, g2, st = read(c / "g1" / "mapping.csv"), read(c / "g2" / "mapping.csv"), read(c / "settlements.csv")
    n, agreed, k = kappa(launch(g1), launch(g2))
    rows = mapping(g1, g2, st)
    if (c / "i1" / "mapping.csv").exists():
        i1, i2 = read(c / "i1" / "mapping.csv"), read(c / "i2" / "mapping.csv")
        ni, ai, ki = kappa(launch(i1), launch(i2))
        print(f"issuer layer: coin-lines {ni}, agreed {ai}, kappa {ki:.3f}")
        layer = issuer_layer(i1, i2, read(c / "issuer-settlements.csv"))
        write(OUT / "variant-fixed-readings-only.csv", FIELDS, rows)
        write(OUT / "variant-series-fixed-readings-only.csv", SERIES_FIELDS, series(rows))
        rows = merge(rows, layer, read(c / "merge-settlements.csv"))
    if (c / "i3" / "mapping.csv").exists():                 # section 17 (G25b): the second issuer layer
        i3, i4 = read(c / "i3" / "mapping.csv"), read(c / "i4" / "mapping.csv")
        n2, a2, k2 = kappa(launch(i3), launch(i4))
        print(f"second issuer layer: coin-lines {n2}, agreed {a2}, kappa {k2:.3f}")
        layer2 = issuer_layer(i3, i4, read(c / "issuer-settlements-2.csv"))
        write(OUT / "variant-after-section-16.csv", FIELDS, rows)
        write(OUT / "variant-series-after-section-16.csv", SERIES_FIELDS, series(rows))
        rows = merge(rows, layer2, read(c / "merge-settlements-2.csv"))
    write(OUT / "mapping.csv", FIELDS, rows)
    lines = series(rows)
    write(OUT / "series.csv", SERIES_FIELDS, lines)
    print(f"launch coin-lines {n}, agreed {agreed}, kappa {k:.3f}; mapping rows {len(rows)}; series lines {len(lines)}")
    print(Counter((r["phase"] == "launch", r["code"]) for r in rows))


if __name__ == "__main__":
    sys.exit(main())
