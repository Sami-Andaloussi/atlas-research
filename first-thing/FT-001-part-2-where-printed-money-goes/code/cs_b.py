"""Card C30 (CS-B, C28's child, an extension): in calm decades, did each point of central-bank money growth go with
less inflation than each point of the public's money, on the same windows?

From the study's folder: ``../../toolkit/bin/ftpy code/cs_b.py``. It refuses to run unless the card is committed and
unchanged (``cards.require_locked``), reads C28's stored points (never recomputes them), and writes its result with
``cards.write_result``. Everything the rule uses is in the card: the calm line, the model, the bootstrap, the checks.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as K  # noqa: E402
import longrun as LR  # noqa: E402

from ft import cards  # noqa: E402

C30 = K.CARDS / "C30-cs-b-base-against-broad.yaml"
C21 = K.CARDS / "C21-a4-1870-named.yaml"
Z = 1.959963984540054
UNION: dict[str, str] = {}  # area -> its union's name, filled from the card's parameters in run()


def cluster(areas: pd.Series) -> np.ndarray:
    """One cluster per currency union, one per area otherwise (the card's item 4)."""
    return pd.factorize(areas.map(lambda a: UNION.get(a, a)))[0]


def common_windows(base_pts: list[dict], broad_pts: list[dict]) -> pd.DataFrame:
    b = pd.DataFrame(base_pts).rename(columns={"mu": "mu_base", "pi": "pi_base", "g": "g_base"})
    m = pd.DataFrame(broad_pts).rename(columns={"mu": "mu_broad", "pi": "pi_broad", "g": "g_broad"})
    d = b.merge(m, on=["area", "y0", "y1"], how="inner")
    bad = d[(d.pi_base - d.pi_broad).abs().gt(1e-9) | (d.g_base - d.g_broad).abs().gt(1e-9)]
    d = d.assign(pi=d.pi_base, g=d.g_base)
    return d, bad


def slope(d: pd.DataFrame, mu: str) -> dict:
    X = sm.add_constant(d[[mu, "g"]].astype(float))
    res = sm.OLS(d.pi.astype(float), X).fit(cov_type="cluster", cov_kwds={"groups": cluster(d.area)})
    b, se = float(res.params[mu]), float(res.bse[mu])
    return {"b": b, "lo": b - Z * se, "hi": b + Z * se}


def stacked_gap(d: pd.DataFrame) -> dict:
    base = d.assign(mu=d.mu_base, D=0.0)
    broad = d.assign(mu=d.mu_broad, D=1.0)
    s = pd.concat([base, broad], ignore_index=True)
    s["muD"], s["gD"] = s.mu * s.D, s.g * s.D
    X = sm.add_constant(s[["D", "mu", "muD", "g", "gD"]].astype(float))
    res = sm.OLS(s.pi.astype(float), X).fit(cov_type="cluster", cov_kwds={"groups": cluster(s.area)})
    b, se = float(res.params["muD"]), float(res.bse["muD"])
    return {"gap": b, "lo": b - Z * se, "hi": b + Z * se}


def bootstrap(d: pd.DataFrame, draws: int, seed: int) -> dict:
    rng = np.random.default_rng(seed)
    key = d.area.map(lambda a: UNION.get(a, a))
    areas = key.unique()
    groups = {a: d[key == a] for a in areas}
    gaps, dcor = [], []
    for _ in range(draws):
        pick = rng.choice(areas, size=len(areas), replace=True)
        x = pd.concat([groups[a] for a in pick], ignore_index=True)
        try:
            gaps.append(slope(x, "mu_broad")["b"] - slope(x, "mu_base")["b"])
            dcor.append(float(np.corrcoef(x.pi, x.mu_broad)[0, 1] - np.corrcoef(x.pi, x.mu_base)[0, 1]))
        except Exception:  # a draw with too few distinct windows: skipped and counted
            continue
    q = lambda v: [float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))]  # noqa: E731
    return {"draws_used": len(gaps), "gap_ci": q(gaps), "dcor_ci": q(dcor)}


def reading(lo: float, hi: float, matters: float) -> str:
    """P03 on an interval against the size that matters (the card's item 7)."""
    if lo > matters:
        return "effect"
    if hi < -matters:
        return "effect of the other sign"
    if lo >= -matters and hi <= matters:
        return "too small to matter"
    return "bounded"


def read_block(d: pd.DataFrame, matters: float, draws: int, seed: int) -> dict:
    if len(d) < 10 or d.area.nunique() < 5:  # a guard on a degenerate split, reported if met
        return {"note": "too few windows", "windows": int(len(d)), "moneys": int(d.area.nunique())}
    sb, sm_ = slope(d, "mu_base"), slope(d, "mu_broad")
    st = stacked_gap(d)
    bs = bootstrap(d, draws, seed)
    cor_b, cor_m = float(np.corrcoef(d.pi, d.mu_base)[0, 1]), float(np.corrcoef(d.pi, d.mu_broad)[0, 1])
    return {"windows": int(len(d)), "moneys": int(d.area.nunique()),
            "clusters": int(d.area.map(lambda a: UNION.get(a, a)).nunique()),
            "share_from_1990": float((d.y0 >= 1990).mean()),
            "slope_base": sb, "slope_broad": sm_, "gap": st, "gap_bootstrap": bs,
            "reading": reading(st["lo"], st["hi"], matters), "refuted": bool(st["gap"] < matters),
            "cor_base": cor_b, "cor_broad": cor_m, "dcor": cor_m - cor_b,
            "var_mu_base": float(d.mu_base.var()), "var_mu_broad": float(d.mu_broad.var())}


def attenuation(block: dict) -> dict | None:
    """The reliability ratio of base growth that would close the gap by measurement error alone (item 9): a limit,
    never a correction."""
    if "gap" not in block:
        return None
    bb, bm = block["slope_base"]["b"], block["slope_broad"]["b"]
    if bm <= 0:
        return {"note": "the broad slope is not positive: no ratio read"}
    return {"reliability_needed": bb / bm, "note": "base's slope over broad's: the share of base growth's variance "
            "that would be signal if the true slopes were equal"}


def jst_block(card: dict, matters: float, draws: int, seed: int) -> dict:
    p = card["parameters"]
    c21 = yaml.safe_load(C21.read_text())
    frame, info = LR.jst_frame(LR.card_gdp_column(c21))
    if frame is None:
        return {"stopped": True, "missing": info["missing"]}
    ends = p["jst_window_ends"]
    nb = LR.windows(frame, "narrowm", ends).rename(columns={"mu": "mu_base"})
    br = LR.windows(frame, "money", ends).rename(columns={"mu": "mu_broad"})
    d = nb.merge(br[["area", "y0", "y1", "mu_broad"]], on=["area", "y0", "y1"], how="inner")
    line = p["calm_line_pct"]
    d = d[(d.mu_base <= line) & (d.mu_broad <= line)]
    wars = p["world_war_years"]
    war = d.apply(lambda r: any(r.y0 < b and r.y1 > a - 1 for a, b in wars), axis=1)
    return {"compares": "JST narrow money (base, notes or M1 by country) against broad money",
            "all": read_block(d, matters, draws, seed),
            "without_world_war_windows": read_block(d[~war], matters, draws, seed)}


def run() -> Path:
    card = yaml.safe_load(C30.read_text())
    cards.require_locked(C30)
    p, mt = card["parameters"], card["matters"]
    UNION.update({a: u for u, members in p["unions"].items() for a in members})
    c28 = json.loads((K.RUNS / "C28-a4-units-guard.json").read_text())["result"]
    if c28.get("void"):
        return cards.write_result(K.STUDY, C30, {"void": True, "why": "C28 is void"})
    d_all, bad = common_windows(c28["C02_grid"]["points"], c28["broad"]["points"])
    if len(bad):
        return cards.write_result(K.STUDY, C30, {"void": True, "why": "base and broad points disagree on pi or g",
                                                 "rows": bad[["area", "y0", "y1"]].to_dict("records")})
    line = p["calm_line_pct"]
    calm = d_all[(d_all.mu_base <= line) & (d_all.mu_broad <= line)].copy()
    draws, seed = p["bootstrap_draws"], p["bootstrap_seed"]
    main = read_block(calm, mt["cs_b_gap"], draws, seed)
    split = p["period_split_year"]
    held_2008 = calm[calm.y1 >= p["era_holds_from"]]  # a window holding a year from 2008 on ends in 2008 or later
    common_2008 = d_all[d_all.y1 >= p["era_holds_from"]]
    dropped_by_base = common_2008[(common_2008.mu_broad <= line) & (common_2008.mu_base > line)]
    out = {
        "void": False,
        "common_windows": int(len(d_all)), "common_moneys": int(d_all.area.nunique()),
        "calm": main, "attenuation": attenuation(main),
        "checks": {
            "from_1990": read_block(calm[calm.y0 >= split], mt["cs_b_gap_from_1990"], draws, seed),
            "to_1990": read_block(calm[calm.y1 <= split], mt["cs_b_gap_to_1990"], draws, seed),
            "era_to_2000": read_block(calm[calm.y1 <= p["era_ends_by"]], mt["cs_b_gap_era_to_2000"], draws, seed),
            "era_from_2008": read_block(held_2008, mt["cs_b_gap_era_from_2008"], draws, seed),
            "jst_1870_1950": jst_block(card, mt["cs_b_gap_jst"], draws, seed),
        },
        "windows_holding_2008": {"common": int(len(common_2008)),
                                 "dropped_by_the_base_rule_alone": int(len(dropped_by_base)),
                                 "dropped_list": sorted(f"{r.area} {r.y0}-{r.y1}"
                                                        for r in dropped_by_base.itertuples())},
        "moneys": sorted(calm.area.unique().tolist()),
    }
    return cards.write_result(K.STUDY, C30, out)


if __name__ == "__main__":
    print(run())
