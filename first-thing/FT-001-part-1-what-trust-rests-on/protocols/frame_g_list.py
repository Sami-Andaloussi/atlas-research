"""FT-001 M7, frame g: the told list (``coins.csv``) from the draft and the person's check (section 6, G5).

The draft (``coins-draft.csv``, ``frame_g.py build --go``) lists every name the fixed readings print; the person's check
(``coders/person-check-<date>.csv``: one decision per draft line, plus the G2 additions, each with its reading, page and
quotation; rechecked by an isolated second reader) decides. This script applies the check, and adds nothing of its own:

- ``keep`` and ``keep, commodity-pegged`` lines are on the list; ``keep, never issued`` too, marked, out of the mapping;
- ``merge with <coin_id>`` adds the line's readings and pages to that coin;
- ``not a coin``, ``governance token`` and ``excluded (Terra)`` are off the list, and ``coins-off.csv`` keeps them with why.

Run from the workshop's root:  toolkit/.venv/bin/python bank/maps/FT-001/missions/code/frame_g_list.py <check.csv>
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
OUT = ROOT / "data" / "reconstructed" / "ft001-g"
ON = ("keep", "keep, commodity-pegged", "keep, never issued")
OFF = ("not a coin", "governance token", "excluded (Terra)")
FIELDS = ("coin_id", "name", "ticker", "readings", "pages", "marks", "check", "check_reading", "check_page", "check_quote")
OFF_FIELDS = ("coin_id", "check", "reading", "page", "quote", "reason")


def apply(draft: list[dict], check: list[dict]) -> tuple[list[dict], list[dict]]:
    """The list and the lines off it. Every draft line needs exactly one decision; an unknown decision is refused."""
    by_id = {r["coin_id"]: r for r in check}
    missing = [d["coin_id"] for d in draft if d["coin_id"] not in by_id]
    if missing:
        raise ValueError(f"draft lines with no decision: {missing}")
    coins: dict[str, dict] = {}
    merges, off = [], []
    for c in check:
        d = next((x for x in draft if x["coin_id"] == c["coin_id"]), None)
        name = d["name"] if d else c["coin_id"].removeprefix("G2: ")
        decision = c["check"].strip()
        if decision in ON:
            marks = "; ".join(m for m in ((d or {}).get("marks", "").replace("governance?", "").strip("; "),
                                          decision.removeprefix("keep").strip(", "), c.get("mark", "")) if m)
            coins[c["coin_id"]] = {
                "coin_id": c["coin_id"].removeprefix("G2: "), "name": name, "ticker": (d or {}).get("ticker", ""),
                "readings": (d or {}).get("readings", "") or c["reading"], "pages": (d or {}).get("pages", "") or c["page"],
                "marks": marks, "check": decision, "check_reading": c["reading"], "check_page": c["page"],
                "check_quote": c["quote"]}
        elif decision.startswith("merge with "):
            merges.append((c, d, decision.removeprefix("merge with ").strip()))
        elif decision in OFF:
            off.append({k: c.get(k, "") for k in OFF_FIELDS})
        else:
            raise ValueError(f"{c['coin_id']}: unknown decision {decision!r}")
    for c, d, target in merges:
        if target not in coins:
            raise ValueError(f"{c['coin_id']}: merge target {target!r} is not on the list")
        t = coins[target]
        t["readings"] = "; ".join(dict.fromkeys(filter(None, t["readings"].split("; ") + [(d or {}).get("readings", "") or c["reading"]])))
        t["pages"] = "; ".join(filter(None, [t["pages"], f"{c['coin_id']}: {(d or {}).get('pages', '') or c['reading'] + ' p.' + c['page']}"]))
    return sorted(coins.values(), key=lambda r: r["coin_id"].lower()), off


def main(argv: list[str]) -> int:
    draft = list(csv.DictReader(open(OUT / "coins-draft.csv", newline="")))
    check = list(csv.DictReader(open(argv[0], newline="")))
    coins, off = apply(draft, check)
    for name, rows, fields in (("coins.csv", coins, FIELDS), ("coins-off.csv", off, OFF_FIELDS)):
        with open(OUT / name, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            w.writerows(rows)
    print(f"{len(coins)} coins on the list, {len(off)} off it")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
