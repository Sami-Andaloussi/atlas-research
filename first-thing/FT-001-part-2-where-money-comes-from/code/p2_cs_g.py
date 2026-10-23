"""Card C38 (CS-G): broad money growth against real growth across C28's ten-year windows, in the manner of Lucas's
Figure 2, C27's filled windows left out; an illustration, no slope read.

From the study's folder: ``python code/p2_cs_g.py``. Writes ``results/runs/C38-cs-g-money-and-real-growth.json``.
"""

from __future__ import annotations

import json
from pathlib import Path

from ft import cards

STUDY = Path(__file__).resolve().parents[1]
CARD = STUDY / "cards" / "C38-cs-g-money-and-real-growth.yaml"
RUNS = STUDY / "results" / "runs"


def main() -> dict:
    card = cards.read(CARD)
    cards.require_locked(CARD)
    line = float(card["parameters"]["calm_line_mu_at_or_below"])
    c28 = json.loads((RUNS / "C28-a4-units-guard.json").read_text())
    if not c28["card_hash"].startswith("99c1880e"):
        raise SystemExit("C38: C28's run is not the one the card names")
    c27 = json.loads((RUNS / "C27-a4-broad-hko-fill.json").read_text())
    if not c27["card_hash"].startswith("6ce96b10"):
        raise SystemExit("C38: C27's run is not the one the card names")
    points = c28["result"]["broad"]["points"]
    added = {(w["area"], w["y0"], w["y1"]) for w in c27["result"]["windows_added"]}
    keys = {(p["area"], p["y0"], p["y1"]) for p in points}
    if not added <= keys:
        raise SystemExit("C38: a window C27 added is not among C28's broad points")
    drawn = [{"area": p["area"], "window": f"{p['y0']}-{p['y1']}", "mu": p["mu"], "g": p["g"], "calm": p["mu"] <= line}
             for p in points if (p["area"], p["y0"], p["y1"]) not in added]
    payload = {"windows_drawn": len(drawn), "windows_left_out": len(points) - len(drawn),
               "monies_drawn": len({d["area"] for d in drawn}), "calm": sum(d["calm"] for d in drawn),
               "not_calm": sum(not d["calm"] for d in drawn),
               "windows": sorted({d["window"] for d in drawn}), "points": drawn}
    cards.write_result(STUDY, CARD, payload)
    return payload


if __name__ == "__main__":
    r = main()
    print(json.dumps({k: v for k, v in r.items() if k != "points"}, indent=1))
