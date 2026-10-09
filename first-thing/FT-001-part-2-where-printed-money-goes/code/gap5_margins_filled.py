"""Gap 5's margin check re-measured on the filled panel (2026-10-02): the same diagnostic as
``gap5_margins.py`` (its definitions, its greedy searches and its tests, imported and unchanged), read on the
filled prices instead of the unfilled ones. A diagnostic, not a card: it tests no claim, writes nothing under
``results/runs`` and changes no verdict. Output: ``notes/gap5-margins-filled-2026-10-02.md`` and the numbers
the long version's Limits tell, ``results/diagnostics/gap5-margins-filled-2026-10-02.json`` (read by
``registry.py``). From the study's folder: ``../../toolkit/bin/ftpy code/gap5_margins_filled.py``.

What is read on what:

- *The deciders*: C26's stored episodes (C15's list re-read on the filled monthly prices; C26's headline, its
  readings and its "every set-apart jump put back" run), in the shape ``gap5_margins.deciders_part`` reads C18's;
  the monthly prices that decide which episodes touch a gap are the filled monthly panel's.
- *A4*: the filled annual panel on C02's grid, on C22's grid (C25's two grids) and on broad money (C27's grid);
  the windows with a CPI gap inside and the windows still lost for a missing CPI at an end are counted on the
  filled panel.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as K  # noqa: E402
import gap5_fill as G  # noqa: E402
import gap5_margins as M  # noqa: E402
import registry as REG  # noqa: E402

DAY = "2026-10-02"
OUT = K.STUDY / "notes" / f"gap5-margins-filled-{DAY}.md"
JSON_OUT = K.STUDY / "results" / "diagnostics" / f"gap5-margins-filled-{DAY}.json"


class _Run:
    """What ``deciders_part`` reads as ``D.C18_RUN``: C18's run, here C26's in C18's shape."""

    def __init__(self, text: str) -> None:
        self.text = text

    def read_text(self) -> str:
        return self.text


def main() -> None:
    a_u, m_u = K.annual(), K.monthly()
    a_f, _, _ = G.filled_annual(a_u)
    m_f, _, _ = G.filled_monthly(m_u, a_u)
    c18 = json.loads(M.D.C18_RUN.read_text())["result"]
    c26 = REG.load("C26-a5-deciders-hko-fill")
    assert not c26["void"]
    as_c18 = {"result": REG._c26_as_c18(c26, c18)}
    M.D.C18_RUN = _Run(json.dumps(as_c18))
    K.annual, K.monthly = (lambda: a_f), (lambda: m_f)
    dec, notes = M.deciders_part([])
    a4, _ = M.a4_part()
    folds = M.a4_folds()
    names = {"C02": "C25 on C02's grid (filled)", "C22": "C25 on C22's grid (filled)", "C03": "C27 (broad money, filled)"}
    for r in a4:
        for k, v in names.items():
            if r[0].startswith(k + " "):
                r[0] = r[0].replace(k, v, 1)
    for r in folds:
        r[0] = {"C02": "C25, C02's grid", "C22": "C25, C22's grid"}[r[0]]
    weak = [r[0] for r in dec if r[9] is not True]
    flips = [f"{r[0]} ({r[10]})" for r in dec if any(f"narrow {k}" in r[10] for k in range(0, 41))]
    # the episodes whose prices still cannot be read at all and that leave the test (the first note's numbers)
    n0 = notes[0]
    unread = {"design": int(n0.split("test (apart, not censored): ")[1].split(" at the design")[0]),
              "m0": int(n0.split("reading, ")[1].split(" at m0")[0])}
    margins = {r[0]: {"stated": r[1], "margin": r[3], "touch": r[4], "lost": r[5], "U": r[6], "robust": r[7], "verdict_without": r[8]}
               for r in a4}
    summary = ("## In one paragraph\n\n"
               f"Deciders' cells with a margin at or below U (narrow, the larger reading), on the filled prices: {len(weak)} of {len(dec)}: "
               + ", ".join(weak) + ". Cells whose verdict flips when only the narrow-U episodes may change side (after putting in "
               f"those that would enter): {len(flips)}: " + ("; ".join(flips) if flips else "none") + ". "
               "Printings whose prices still cannot be read at all and that leave the test: "
               f"{unread['design']} at the design's reading, {unread['m0']} at m0. A4, on the filled panel: "
               + "; ".join(f"{k}: margin {v['margin']} against U {v['U']}" for k, v in margins.items()) + ".\n")
    txt = [f"# Gap 5's margin check re-measured on the filled panel ({DAY})", "",
           "A diagnostic, not a card (`code/gap5_margins_filled.py`: the definitions, searches and tests of "
           "`code/gap5_margins.py`, unchanged; C26's stored episodes and the filled annual and monthly panels). It tests no "
           "claim, writes no result under `results/runs` and changes no verdict; the earlier note, "
           "`notes/gap5-margins-2026-10-02.md`, stays as it was, on the unfilled panel. **A greedy margin is an upper bound of "
           "the true minimum**: a margin at or below U is a definite weakness; a margin above U, with no flip found, is "
           "evidence, not proof. In A4's table, U counts the headline's windows with a CPI gap inside plus the grid's windows "
           "still lost for a missing CPI at an end after the fill.", "",
           summary,
           "## The deciders' 12 cells (C26's headline on the filled prices; both accommodation readings)", "",
           M.table(["cell", "stated verdict", "each reading", "margin per reading (changes of side)", "kind",
                    "margin used", "uncertain U per reading (touch a price gap + would enter)", "U used (larger)",
                    "U wide (+ other episodes of the 15 economies)", "margin > U?",
                    "swaps found, when only the U episodes may change side (narrow; wide), after putting the would-enter episodes in",
                    "C26's 'every set-apart jump put back'"], dec),
           "", *[f"- {n}" for n in notes], "",
           "## A4 headline slopes (one window removed = one change)", "",
           M.table(["verdict", "stated", "greedy removals to flip, by direction", "margin", "windows with a CPI gap inside",
                    "windows lost only for a missing CPI at an end (after the fill)", "U", "margin > U?",
                    "verdict with the windows that have a CPI gap inside removed"], a4), "",
           "## A4 folds (the failure clause: two or more folds telling another verdict)", "",
           M.table(["card", "headline verdict", "folds", "folds that must change", "each fold",
                    "windows to change the statement (sum of the smallest)"], folds), ""]
    OUT.write_text("\n".join(txt))
    JSON_OUT.parent.mkdir(parents=True, exist_ok=True)
    JSON_OUT.write_text(json.dumps({
        "kind": "diagnostic, not a card: no claim is tested", "date": DAY,
        "deciders": {"cells": len(dec), "margin_at_or_below_U": len(weak), "weak_cells": weak,
                     "flip_when_only_narrow_U_change": len(flips), "flip_cells": flips, "unread_leaving_the_test": unread,
                     "rows": dec},
        "a4": margins, "a4_folds": folds}, indent=1, default=str))
    print(OUT)


if __name__ == "__main__":
    main()
