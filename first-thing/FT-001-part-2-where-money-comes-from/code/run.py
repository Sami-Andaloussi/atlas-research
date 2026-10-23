"""Recompute every number and figure of part 2 (the rebuild of 2026-10-10); from the study's folder:
python code/run.py

The rebuild's cards run first, each refusing to run unless its card is committed and unchanged, and each writing
``results/runs/<card>.json`` with the card's hash: C35 (CS-A, ``p2_cs_a.py``), C36 (CS-E, ``p2_cs_e.py``), C37 (CS-F,
``p2_cs_f.py``), C38 (CS-G, ``p2_cs_g.py``, on C28's stored windows) and C39 (K11's count,
``p2_k11_base.py``, on the same windows). The reused cards are read, not rerun: C28 and
C29 (CS-C, ``units_guard.py``), C30 (CS-B, ``cs_b.py``) and C31 (CS-D, ``cs_e.py``); each refuses a changed card if
rerun. Then ``p2_registry.py`` writes every printed number and every claim into ``results/numbers.json``,
``p2_figures.py`` draws the figures and the balance-sheet explorer, and ``p2_og.py`` the preview image.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import p2_cs_a  # noqa: E402
import p2_cs_e  # noqa: E402
import p2_cs_f  # noqa: E402
import p2_cs_g  # noqa: E402
import p2_figures  # noqa: E402
import p2_k11_base  # noqa: E402
import p2_og  # noqa: E402
import p2_registry  # noqa: E402


def main() -> None:
    p2_cs_a.main()  # C35
    p2_cs_e.main()  # C36
    p2_cs_f.main()  # C37
    p2_cs_g.main()  # C38
    p2_k11_base.main()  # C41 (C39 corrected: Kazakhstan's splice, 2026-10-22)
    p2_registry.main()
    p2_figures.main()
    p2_og.main()


if __name__ == "__main__":
    main()
