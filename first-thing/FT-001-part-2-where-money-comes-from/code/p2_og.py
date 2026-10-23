"""The web study's preview image, ``web/site/<slug>/images/og.png`` (1200 x 630): the title and the open answer
in the house style. From the study's folder: ``python code/p2_og.py``."""

from __future__ import annotations

import json
import re
import textwrap
from pathlib import Path

import matplotlib.pyplot as plt

from ft.charts import style

STUDY = Path(__file__).resolve().parent.parent
SITE = STUDY / "web" / "site" / "ft-001-part-2-where-money-comes-from"


def main() -> Path:
    style.apply()
    t = style.TOKENS
    meta = json.loads((SITE / "meta.json").read_text())
    fig = plt.figure(figsize=(12, 6.3), dpi=100)
    fig.patch.set_facecolor(t["bg"])
    fig.text(0.06, 0.86, "FIRST THING  ·  WEEKLY STUDY", fontsize=15, color=t["green"], fontweight=600,
             fontfamily=style.SANS_STACK)
    fig.text(0.06, 0.70, meta["title"], fontsize=46, color=t["ink"], fontweight=600, fontfamily=style.SERIF_STACK,
             va="top")
    body = ""  # the standfirst's whole sentences, as many as fit in four lines above the footer rule
    for sentence in re.split(r"(?<=\.)\s+", meta["standfirst"].strip()):
        candidate = f"{body} {sentence}".strip()
        if body and len(textwrap.wrap(candidate, 62)) > 4:
            break
        body = candidate
    body = textwrap.fill(body, 62)
    fig.text(0.06, 0.48, body, fontsize=21, color=t["muted"], fontfamily=style.SANS_STACK, va="top", linespacing=1.45)
    fig.add_artist(plt.Line2D([0.06, 0.94], [0.10, 0.10], color=t["rule"], linewidth=1.2))
    fig.text(0.06, 0.05, "The life of a money · part 2", fontsize=14, color=t["muted"], fontfamily=style.SANS_STACK)
    out = SITE / "images" / "og.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=100, facecolor=t["bg"])
    plt.close(fig)
    return out


if __name__ == "__main__":
    main()
