"""Card C34 (CS-C's correction): job openings per unemployed person from BLS's own series, over C32's quarters.

From the study's folder: ``../../toolkit/bin/ftpy code/cs_c_vu.py``. Writes ``results/runs/C34-cs-c-vu-bls.json``.

Readings of the card that its text leaves to the code, fixed here before the run:

- *A month's ratio*: JTSJOL over UNEMPLOY, both in thousands, the month's value as FRED gives it.
- *C32's quarters*: the keys of C32's ``timeline.quarterly`` and ``stretch.quarterly``, in order; they must run
  without a gap from the card's first quarter to its last, or the run is void.
- *The comparison beside*: computed against C32's stored v/u and written as two numbers only (the largest absolute
  difference and the correlation); no quarter of theirs is written.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as K  # noqa: E402

from ft import cards  # noqa: E402

CARD = K.CARDS / "C34-cs-c-vu-bls.yaml"
C32 = K.RUNS / "C32-cs-c-door-timeline.json"


def main() -> Path:
    prm = yaml.safe_load(CARD.read_text())["parameters"]
    c32 = json.loads(C32.read_text())["result"]
    theirs = {**{q: v["v_over_u"] for q, v in c32["timeline"]["quarterly"].items()},
              **{q: v["v_over_u"] for q, v in c32["stretch"]["quarterly"].items()}}
    quarters = pd.period_range(prm["first_quarter"], prm["last_quarter"], freq="Q")
    if [str(q) for q in quarters] != sorted(theirs):
        return cards.write_result(K.STUDY, CARD, {"void": True, "why": "C32's quarters are not the card's, without a gap"})
    v = K.fred_monthly("JTSJOL", "2026-10-09")
    u = K.fred_monthly("UNEMPLOY", "2026-10-09")
    ratio = (v / u).dropna()
    out, missing = {}, []
    for q in quarters:
        months = pd.period_range(q.asfreq("M", "start"), q.asfreq("M", "end"), freq="M")
        if not all(m in ratio.index for m in months):
            missing.append(str(q))
            continue
        out[str(q)] = float(np.mean([ratio[m] for m in months]))
    if missing:
        return cards.write_result(K.STUDY, CARD, {"void": True, "why": "quarters lacking a month", "quarters": missing})
    ours = pd.Series(out)
    theirs_s = pd.Series({q: float(theirs[q]) for q in out})
    gap = float((ours - theirs_s).abs().max())
    return cards.write_result(K.STUDY, CARD, {
        "void": False,
        "units": "job openings per unemployed person (JOLTS JTSJOL over UNEMPLOY, both thousands, seasonally adjusted)",
        "quarterly": out,
        "beside_c32": {"largest_absolute_difference": gap, "correlation": float(ours.corr(theirs_s)),
                       "passes_0_1": gap > 0.1,
                       "note": "against C32's v/u from Blanchard and Bernanke's files; none of their quarters written"},
        "first_month": str(ratio.index.min()), "last_month": str(ratio.index.max())})


if __name__ == "__main__":
    print(main())
