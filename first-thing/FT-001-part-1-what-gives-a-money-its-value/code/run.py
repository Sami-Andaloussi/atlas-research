"""Recompute every number and figure of part 1 (the rebuild of 2026-10-10); from the study's folder:
python code/run.py

The rebuild's cards run first, each refusing to run unless its card is committed and unchanged, and each writing
``results/runs/<card>.json`` with the card's hash: C21 (CS-A, ``p1_cs_a.py``), C22 (CS-B, ``p1_cs_b.py``) and C23
(CS-C, ``p1_cs_c.py``, which rebuilds frame b's panel and checks its digest), then C24 (CS-C's years in crisis,
``p1_cs_c_years.py``, on C23's denominator), and C25 (K9's count,
``p1_k9_debt.py``, on JST R6). The reused cards are read, not rerun:
C18 (CS-F, ``cs_a.py``), C19 and C20 (CS-D, ``cs_b.py`` and ``cs_b_trim.py``); each refuses a changed card if rerun.
Then ``p1_registry.py`` writes every printed number and every claim into ``results/numbers.json``, ``p1_figures.py``
draws the figures and ``p1_web.py`` writes the web study's folder for ``ft study web``.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import p1_cs_a  # noqa: E402
import p1_cs_b  # noqa: E402
import p1_cs_c  # noqa: E402
import p1_cs_c_years  # noqa: E402
import p1_k9_debt  # noqa: E402
import p1_registry  # noqa: E402


def main() -> None:
    p1_cs_a.main()      # C21
    p1_cs_b.main()      # C22
    p1_cs_c.main()      # C28 (C23 corrected: Kazakhstan's splice, 2026-10-22)
    p1_cs_c_years.main()  # C29 (C24 corrected)
    p1_k9_debt.main()   # C25
    p1_registry.main()
    for name in ("p1_figures", "p1_og", "p1_web"):
        try:
            module = __import__(name)
        except ModuleNotFoundError:
            continue
        module.main()


if __name__ == "__main__":
    main()
