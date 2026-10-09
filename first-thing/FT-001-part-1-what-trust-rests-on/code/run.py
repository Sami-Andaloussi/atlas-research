"""Recompute every number and figure of part 1; from the study's folder:
../../toolkit/bin/ftpy code/run.py

The cards run in this order: C15 (claim 1's dated lines with the limit by institution by M0's text; C07's and C04's
runs stay in git beside it), C05
(claim 2 on frame c's coding of the supports), C11 (C05's reading without pegs, the CFA unions' members out), C13
(claim 2 with the limit by institution read by M0's text: the reading printed, C05's and C11's beside it) and C14 (the
dollar, the euro, bitcoin and the stablecoins today: C12 with the limit by institution read by M0's text; C06, C08,
C09, C10 and C12 before it stay in git). Each refuses to run unless its card is committed and
unchanged, and writes ``results/runs/<card>.json`` naming the card's hash. Then ``registry.py`` writes every printed
number into ``results/numbers.json`` (reading also the committed builds of A3, the window, frame k and frame g, whose
protocols are their cards), ``readings.py`` adds each claim's reading and each printed number's labels (the
regeneration, 2026-10-07), ``claims.py`` writes map v11's claims (round 2), and ``figures.py`` and ``figures_v11.py``
draw every figure into ``results/figures/``; ``web_v11.py`` writes the web study's folder (map v11's figures,
the calculator, glossary, meta and og.png) for ``ft study web``.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import claim1  # noqa: E402
import claim2  # noqa: E402
import claims  # noqa: E402
import figures  # noqa: E402
import figures_v11  # noqa: E402
import now  # noqa: E402
import readings  # noqa: E402
import registry  # noqa: E402
import web_v11  # noqa: E402


def main() -> None:
    claim1.main()     # C15 (C07: claim1.main(claim1.CARD_V2); C04: claim1.main(claim1.CARD))
    claim2.main()     # C05
    claim2.main(claim2.CARD_CFA)  # C11
    claim2.main(claim2.CARD_M0)   # C13
    now.main()        # C14 (C06 as it ran: now.main(now.CARD); C12: now.main(now.CARD_V5))
    # map v11's cards (round 2) ran at step c and are read, not rerun here: C16 (code/cs_d.py), C18 (code/cs_a.py),
    # C19 (code/cs_b.py), C20 (code/cs_b_trim.py); C17 (code/cs_e_second.py) is void; each refuses a changed card
    registry.main()   # with registry_v11 (C16-C20) and sources_v11 (cited numbers, frozen data)
    readings.apply()  # each claim's reading and each printed number's labels (2026-10-07)
    claims.apply()    # map v11's claims (round 2): each typed, scoped, on its sources' passages or its card
    figures.main()
    figures_v11.main()  # map v11's figures: CS-A, CS-B, CS-D
    web_v11.main()      # the web study's folder (step w, round 2)


if __name__ == "__main__":
    main()
