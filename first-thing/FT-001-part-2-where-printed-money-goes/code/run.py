"""Recompute every number and figure of the study; from the study's folder:
../../toolkit/bin/ftpy code/run.py

The cards run in the order STATE fixes for step d: C15 (frame e's list, entry side), then C18 (what
decided whether added base money reached prices and broad money), C24 (the same with the wars before 1989 coded), C13 (what inflation took from cash and
from deposits that paid nothing), C19 (velocity), and C01 (the door) with C02-C04, C21, C22 and C23 (the long run), then C25 and C26 (the same two tests with the CPI gaps filled, ``gap5_fill.py``), C27 (broad money on the same fill), C28 (the units guard) and C29 (its exploration, ``units_guard.py``). Each
refuses to run unless its card is committed and unchanged, and writes ``results/runs/<card>.json`` naming
the card's hash. Then ``registry.py`` writes every printed number into ``results/numbers.json``, ``readings.py`` adds each
claim's reading and each printed number's labels (2026-10-06), and
``figures.py`` draws every figure into ``results/figures/``.

``code/panel.py`` builds the panels (its rules at its top); ``code/common.py`` builds them once per run.
C05 and C09 (``code/episodes.py``) ran at step c; their results are read, not rerun.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import claims  # noqa: E402
import deciders  # noqa: E402
import door  # noqa: E402
import figures  # noqa: E402
import figures_v15  # noqa: E402
import frame_e  # noqa: E402
import gap5_fill  # noqa: E402
import longrun  # noqa: E402
import readings  # noqa: E402
import registry  # noqa: E402
import tax  # noqa: E402
import units_guard  # noqa: E402
import velocity  # noqa: E402
import web_v15  # noqa: E402


def main() -> None:
    frame_e.main()   # C15
    deciders.main()  # C18
    deciders.war()   # C24 (C18's war-out run with the wars of 1946-1988 coded; reads C18's committed run)
    tax.main()       # C13
    velocity.main()  # C19
    door.main()      # C01
    longrun.main()   # C02, C03, C04, C21, C22
    gap5_fill.c25()  # C25 (C02's model with the annual CPI gaps filled from the World Bank's inflation database)
    gap5_fill.c26()  # C26 (C24's run with the monthly CPI gaps filled; about twelve minutes)
    gap5_fill.c27()  # C27 (C03's broad money on C25's fill rule)
    units_guard.c28()  # C28 (C25 and C27 with the units guard on the World Bank fills)
    units_guard.c29()  # C29 (the exploration of C28's windows, its fifteen slices)
    # map v15's cards (round 2) ran at step c and are read, not rerun here: C30 (code/cs_b.py), C31 (code/cs_e.py,
    # about two hours), C32 (code/cs_c.py), C33 (code/cs_f.py), C34 (code/cs_c_vu.py); each refuses to run on a changed card
    registry.main()
    readings.apply()  # the readings and labels (2026-10-06, the regeneration): fields added, no value changed
    claims.apply()  # map v15's claims (round 2): each typed, scoped, on its sources' passages or its card
    figures.main()
    figures_v15.main()  # map v15's figures: the door's timeline and decomposition, CS-B, CS-E
    web_v15.main()  # map v15's web study: its figures, calculator, glossary, meta and og.png (round 1's web.py
    # holds the helpers it reuses)


if __name__ == "__main__":
    main()
