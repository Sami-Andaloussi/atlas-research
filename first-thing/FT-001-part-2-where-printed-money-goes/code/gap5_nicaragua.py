"""One window of the fill carries two verdict changes (2026-10-02): a diagnostic, not a card (it tests no claim and
changes no verdict; the filled reading stays the reading, its rule having been fixed before the outcome).

The narrow re-check (``check/2026-10-02-opus-filled-prices-recheck.md``, finding 1) found that the move of C22's grid
(decades to 2019) from "partly" to one for one rests on NI 1979-89, and that broad money's held-out decades from
1990 ("partly" to one for one) rest on NI 1990-2000: both are windows the fill adds, whose end prices are the
database's chained annual rates. This reads each filled run again without its window, with the functions of
``gap5_fill.py`` and ``longrun.py`` unchanged. Output: ``notes/gap5-nicaragua-2026-10-02.md`` and
``results/diagnostics/gap5-nicaragua-2026-10-02.json`` (read by ``registry.py``). From the study's folder:
``../../toolkit/bin/ftpy code/gap5_nicaragua.py``.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as K  # noqa: E402
import gap5_fill as G  # noqa: E402
import longrun as L  # noqa: E402

DAY = "2026-10-02"
OUT = K.STUDY / "notes" / f"gap5-nicaragua-{DAY}.md"
JSON_OUT = K.STUDY / "results" / "diagnostics" / f"gap5-nicaragua-{DAY}.json"


def reading(df, drop: tuple | None) -> dict:
    d = df if drop is None else df[~((df.area == drop[0]) & (df.y0 == drop[1]) & (df.y1 == drop[2]))]
    head = L.headline(d)
    ho = L.held_out(d, head)
    t = ho["test"]
    return {"windows": int(len(d)), "beta": head["beta"], "lo": head["beta_lo"], "hi": head["beta_hi"], "verdict": head["verdict"],
            "held_out_beta": t["beta"], "held_out_lo": t["beta_lo"], "held_out_hi": t["beta_hi"], "held_out_verdict": t["verdict"],
            "folds_differing": ho["folds_differing"]}


def main() -> None:
    a = K.annual()
    a_f, _, sources = G.filled_annual(a)
    f = a_f[~a_f.units_break]
    ends22 = yaml.safe_load(G.C25.read_text())["parameters"]["window_ends_beside_C22"]
    ends03 = yaml.safe_load(G.C27.read_text())["parameters"]["window_ends"]
    out = {"kind": "diagnostic, not a card: no claim is tested, no verdict changed", "date": DAY}
    for tag, money, ends, win in (("c22", "base", ends22, ("NI", 1979, 1989)), ("broad_ho", "broad", ends03, ("NI", 1990, 2000))):
        df = L.windows(f, money, ends)
        row = df[(df.area == win[0]) & (df.y0 == win[1]) & (df.y1 == win[2])].iloc[0]
        out[tag] = {"window": f"{win[0]} {win[1]}-{win[2]}", "mu": float(row.mu), "pi": float(row.pi),
                    "cpi_source_y0": sources.get((win[0], win[1]), "panel"), "cpi_source_y1": sources.get((win[0], win[2]), "panel"),
                    "with": reading(df, None), "without": reading(df, win)}
    # the decades to 2020 (C25 on C02's grid) without every Nicaraguan window: the main reading is not touched
    ends02 = yaml.safe_load(G.C25.read_text())["parameters"]["window_ends"]
    df02 = L.windows(f, "base", ends02)
    h_all, h_no = L.headline(df02), L.headline(df02[df02.area != "NI"])
    out["c02_without_nicaragua"] = {"windows_with": int(len(df02)), "windows_without": int((df02.area != "NI").sum()),
                                    "beta_with": h_all["beta"], "beta": h_no["beta"], "lo": h_no["beta_lo"], "hi": h_no["beta_hi"],
                                    "verdict": h_no["verdict"]}
    JSON_OUT.parent.mkdir(parents=True, exist_ok=True)
    JSON_OUT.write_text(json.dumps(out, indent=1))

    def line(t, label):
        x = out[t]
        w, wo = x["with"], x["without"]
        return (f"- **{label}** ({x['window']}; money growth {x['mu']:.0f}% and inflation {x['pi']:.0f}% a year; the CPI at its two ends "
                f"from: {x['cpi_source_y0']}, {x['cpi_source_y1']}). With it: headline {w['beta']:.3f} ({w['lo']:.3f} to {w['hi']:.3f}), "
                f"{w['verdict']}; held out {w['held_out_beta']:.3f} ({w['held_out_lo']:.4f} to {w['held_out_hi']:.4f}), {w['held_out_verdict']}. "
                f"Without it: headline {wo['beta']:.3f} ({wo['lo']:.3f} to {wo['hi']:.3f}), {wo['verdict']}; held out "
                f"{wo['held_out_beta']:.3f} ({wo['held_out_lo']:.4f} to {wo['held_out_hi']:.4f}), {wo['held_out_verdict']}.")
    OUT.write_text("\n".join([
        f"# One Nicaraguan window under two verdict changes ({DAY})", "",
        "A diagnostic, not a card (`code/gap5_nicaragua.py`): the filled runs of C25 (C22's grid) and C27 (held-out decades from 1990) "
        "read again without the one window the narrow re-check named for each. It tests no claim and changes no verdict: the filled "
        "reading stays the reading, because its rule was fixed before the outcome and removing a window now would be revising toward "
        "an answer (BLUEPRINT 11.15). It is told as a fragility.", "",
        line("c22", "Decades to 2019 (C25 on C22's grid)"), line("broad_ho", "Broad money's held-out decades from 1990 (C27)"),
        f"- **The decades to 2020 (C25 on C02's grid), without every Nicaraguan window**: {out['c02_without_nicaragua']['beta']:.3f} "
        f"({out['c02_without_nicaragua']['lo']:.3f} to {out['c02_without_nicaragua']['hi']:.3f}), {out['c02_without_nicaragua']['verdict']} "
        f"(with them {out['c02_without_nicaragua']['beta_with']:.3f}): the main reading does not rest on them.", ""]))
    print(OUT)


if __name__ == "__main__":
    main()
