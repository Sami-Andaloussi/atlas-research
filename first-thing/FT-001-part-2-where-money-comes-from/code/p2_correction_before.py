"""The values printed before the correction of 2026-10-21, extracted once from the project's history into a committed
file, so that the correction note's "before" figures are read, never typed, and reproduce without that history.

From the study's folder: ``python code/p2_correction_before.py``. Reads, at the project's commit
``PRE_CORRECTION`` (the last before the correction), ``results/numbers.json`` (the registry as printed then) and
``results/runs/C28-a4-units-guard.json`` (Kazakhstan's 2010-2020 window), and writes
``results/correction-2026-10-21-before.json``. Run where that commit exists (the project); ``p2_registry.py`` reads the
file it writes, never the history. Refuses to overwrite a file whose values differ.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

STUDY = Path(__file__).resolve().parents[1]
OUT = STUDY / "results" / "correction-2026-10-21-before.json"
PRE_CORRECTION = "7c378b06"   # the project's commit before the correction of 2026-10-21
KEYS = ("lr_x_s7", "lr_broad_mu_below", "cs-c_lr_broad_below_lo", "cs-c_lr_broad_below_hi", "k11b_s2_hit10",
        "k11b_all_hit10")


def _show(rel: str) -> dict:
    top = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=STUDY, capture_output=True, text=True,
                              check=True).stdout.strip())
    path = (STUDY / rel).resolve().relative_to(top.resolve()).as_posix()
    return json.loads(subprocess.run(["git", "show", f"{PRE_CORRECTION}:{path}"], cwd=top, capture_output=True,
                                     text=True, check=True).stdout)


def extract() -> dict:
    numbers = _show("results/numbers.json")["numbers"]
    c28 = _show("results/runs/C28-a4-units-guard.json")["result"]
    kz = next(q for q in c28["C02_grid"]["points"] if q["area"] == "KZ" and q["y0"] == 2010)
    return {"commit": PRE_CORRECTION, "written_by": "code/p2_correction_before.py",
            "what": "values as the study printed them before the correction of 2026-10-21 (results/numbers.json and "
                    "results/runs/C28-a4-units-guard.json at the commit named), extracted by script, never typed",
            "numbers": {k: numbers[k]["value"] for k in KEYS},
            "C28_KZ_2010_2020_pi": kz["pi"]}


def main() -> None:
    body = extract()
    if OUT.exists() and json.loads(OUT.read_text()) != body:
        sys.exit(f"{OUT.name} exists with other values: not overwritten")
    OUT.write_text(json.dumps(body, indent=2, sort_keys=True) + "\n")
    print(f"wrote {OUT.relative_to(STUDY)}")


if __name__ == "__main__":
    main()
