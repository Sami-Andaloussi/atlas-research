"""Card C41 (C39 corrected: Kazakhstan's splice, 2026-10-22; K11, a base rate): of C28's ten-year windows in each band of base money
growth, how many had inflation averaging a fifth a year or more over the decade (a tenth, a variant); counts, shares,
cluster-bootstrap intervals.

From the study's folder: ``python code/p2_k11_base.py``. Writes
``results/runs/C41-k11-inflation-by-money-pace-kazakhstan.json``.
"""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import numpy as np

from ft import cards

STUDY = Path(__file__).resolve().parents[1]
CARD = STUDY / "cards" / "C41-k11-inflation-by-money-pace-kazakhstan.yaml"  # C39 corrected (2026-10-22)
RUNS = STUDY / "results" / "runs"
C28 = RUNS / "C28-a4-units-guard.json"
C28_SHA = "23550f4072dcc03f778e15a3bbe64e98bbeb6fb3ff42e1172c242511119e0d97"  # C28 rerun with Kazakhstan's splice (2026-10-22)
DENOMINATORS = [309, 203, 78, 31, 14]


def _band_of(mu: float, bands: list) -> int:
    for i, (lo, hi) in enumerate(bands):
        if (lo is None or mu > lo) and (hi is None or mu <= hi):
            return i
    raise SystemExit(f"C41: mu {mu} falls in no band")


def _merge(bands: list, counts: list[int], floor: int) -> list[list[int]]:
    """Groups of band indices: from the top band down, a band under ``floor`` joins the band below; a bottom band
    under ``floor`` joins the band above."""
    groups = [[i] for i in range(len(bands))]
    size = list(counts)
    i = len(groups) - 1
    while i > 0:
        if size[i] < floor:
            groups[i - 1] += groups[i]
            size[i - 1] += size[i]
            del groups[i], size[i]
        i -= 1
    if len(groups) > 1 and size[0] < floor:
        groups[1] = groups[0] + groups[1]
        size[1] += size[0]
        del groups[0], size[0]
    return groups


def _stat(windows: list[dict], line_pi: float, draws: int) -> dict:
    rng = np.random.default_rng(20261012)  # the card's generator, fresh for each band and line
    areas = sorted({w["area"] for w in windows})
    by_area = {a: [w for w in windows if w["area"] == a] for a in areas}
    hits = [sum(1 for w in by_area[a] if w["pi"] >= line_pi) for a in areas]
    sizes = [len(by_area[a]) for a in areas]
    n, k, m = len(windows), sum(hits), len(areas)
    out = {"windows": n, "areas": m, "at_or_above": k, "share": 100 * k / n}
    if k == 0:
        out["bound"] = {"kind": "at most", "value": 100 * (1 - 0.05 ** (1 / m))}
    elif k == n:
        out["bound"] = {"kind": "at least", "value": 100 * 0.05 ** (1 / m)}
    else:
        h, s = np.array(hits), np.array(sizes)
        shares = []
        for _ in range(draws):
            pick = rng.integers(0, m, size=m)
            shares.append(100 * h[pick].sum() / s[pick].sum())
        lo, hi = np.percentile(shares, [2.5, 97.5])
        out["low"], out["high"] = float(lo), float(hi)
    return out


def main() -> dict:
    card = cards.read(CARD)
    cards.require_locked(CARD)
    p = card["parameters"]
    if hashlib.sha256(C28.read_bytes()).hexdigest() != C28_SHA:
        raise SystemExit("C41: C28's run is not the one the card names (sha256)")
    c28 = json.loads(C28.read_text())
    if not c28["card_hash"].startswith("99c1880e"):
        raise SystemExit("C41: C28's run is not the one the card names (card_hash)")
    points = c28["result"]["C02_grid"]["points"]
    if len(points) != 635 or len({q["area"] for q in points}) != 155:
        raise SystemExit("C41: C28's base points are not 635 in 155 areas")
    if any(q.get("mu") is None or q.get("pi") is None for q in points):
        raise SystemExit("C41: a point lacks mu or pi")
    bands = p["bands_mu"]
    idx = [_band_of(q["mu"], bands) for q in points]
    counts = [idx.count(i) for i in range(len(bands))]
    if counts != DENOMINATORS:
        raise SystemExit(f"C41: band denominators {counts}, not {DENOMINATORS}")
    groups = _merge(bands, counts, int(p["merge_below_windows"]))
    if groups != [[0], [1], [2], [3, 4]]:
        raise SystemExit(f"C41: the merge gives {groups}, not the band named on the card")
    lines = {name: 100 * math.log(1 + v) for name, v in p["lines"].items()}
    result: dict = {"lines_pi": lines, "bands": [], "all": {}}
    for g in groups:
        lo, hi = bands[g[0]][0], bands[g[-1]][1]
        members = [q for q, i in zip(points, idx) if i in g]
        entry = {"band": {"above": lo, "at_or_below": hi}}
        for name, line_pi in lines.items():
            entry[name] = _stat(members, line_pi, 2000)
        result["bands"].append(entry)
    for name, line_pi in lines.items():
        result["all"][name] = _stat(points, line_pi, 2000)
    cards.write_result(STUDY, CARD, result)
    return result


if __name__ == "__main__":
    print(json.dumps(main(), indent=1))
