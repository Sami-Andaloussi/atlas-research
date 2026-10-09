"""Card C17 (CS-E's second coder, C14's child): a different model codes a quarter of frame g's coins at launch.

From the study's folder, in this order:
- ``../../toolkit/bin/ftpy code/cs_e_second.py draw`` writes the sample to ``data/reconstructed/ft001-g/coders/x1/
  sample.csv`` (committed before the coder starts);
- ``... cs_e_second.py stage <folder>`` builds the coder's staged folder outside the workshop and writes
  ``x1/stage-manifest-run2.json`` (each staged file's sha256 and the rename table; committed before the coder runs);
- the coder writes ``<folder>/out/codes.csv``; the session moves it to ``x1/mapping.csv``;
- ``... cs_e_second.py isolation <transcript.jsonl> <folder>`` writes ``x1/isolation-run2.json`` from the coder's tool calls;
- ``... cs_e_second.py blind`` writes ``x1/blind-key.csv`` and the reader's list ``x1/reader-input.csv``;
- after the third reader's ``x1/readings.csv`` exists, ``... cs_e_second.py compare`` writes
  ``results/runs/C17-cs-e-second-model.json``.

Readings of the card that its text leaves to the code, fixed here before the run:

- *A code*: ``yes``, ``no`` or ``cannot be read``, compared after stripping and lower-casing.
- *Settled launch code*: mapping.csv's row for (coin_id, line) with phase ``launch``.
- *Kappa*: Cohen's, from the 3 x 3 table of the coder's codes against the settled ones on the sampled coin-lines both
  give.
- *The third reader's file* (``x1/readings.csv``): one row per disagreement, ``coin_id,line,verdict,rule,passage``
  with verdict ``A``, ``B``, ``neither`` or ``cannot settle``; ``x1/blind-key.csv`` (``coin_id,line,coder_is``) says
  which letter was the coder's, drawn by the seed and written before the reader runs.
- *A stratum*: a coin whose coin_id an issuer sheet names (either issuer packet).
- *The origin* of a settled code (mapping.csv's ``settled`` column): the S-rule it names (the first ``S<n>``), else
  "agreed (issuer layer)" where it says ``issuer``, else "agreed (first layer)".
- *Wrong at its document*: the reader's verdict names the coder's code, or ``neither``; in C14's variant the coder's
  code replaces the settled one, and ``neither`` enters as cannot be read.
- *The staged folder*: ``instructions/`` (``00-output.md``, the one output specification; M7 sections 3, 9, 14 and 17 at
  7b9fc9da; the packet and issuer READMEs), ``sheets/`` (the sampled coins' packet and issuer sheets), ``docs/`` (every
  frozen file those sheets name: an issuer sheet's listed files; a reading's document files, its manifests left out,
  for each label a sampled packet sheet names), ``out/``. Every staged text is rewritten: a frozen file's path or name
  becomes its neutral name, a reading's folder its neutral names (an unstaged reading reads "not staged"), any other
  path in backquotes "(not staged)", a commit id "(a commit)".
- *Isolation* (on the tool calls' paths, never on a command's other words or a file's content): every Read, Glob,
  Grep, Edit or Write path (and a Glob pattern) is absolute and inside the staged folder; every Bash command begins
  ``cd <stage> &&``, holds no other ``cd``, no ``..``, no ``~`` or ``$`` path, and every absolute path in it lies
  inside the stage; no path holds an ``isolation_terms`` word; no web tool is called. Otherwise the run is void.
- *The reader's places*: both sides' sources and locators, split on ``|`` and ``;``, the ``who:`` notes dropped,
  merged into one sorted list without attribution (so the layout cannot tell which code is the coder's).
- *who may redeem*: compared where the settled launch redemption is yes and who-classes.csv has a class; a coin it
  marks ``not settled`` is listed apart, never counted as a disagreement.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import shutil
import subprocess
import sys
from collections import Counter
from pathlib import Path

import numpy as np
import yaml

HERE = Path(__file__).resolve().parent
STUDY = HERE.parent
ROOT = STUDY.parents[1]
G = ROOT / "data" / "reconstructed" / "ft001-g"
X1 = G / "coders" / "x1"
CARD = STUDY / "cards" / "C17-cs-e-second-model.yaml"
CODES = ("yes", "no", "cannot be read")
#: The card's item 7: run 1 is void by its isolation rule and is never used; run 2's files carry this suffix (its
#: manifest, its isolation check). The coder's codes of run 2 are moved to ``x1/mapping.csv``.
RUN = "-run2"
BLIND_SEED = 20261009  # the card's item 5: one draw per disagreement, in the comparison's order
M7 = "bank/maps/FT-001/missions/FT-001-M7-frame-g.md"
M7_AT = "7b9fc9da"
M7_SECTIONS = (3, 9, 14, 17)
FROZEN = ROOT / "data" / "frame-g"


def read_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def slug(name: str) -> str:
    return "".join(ch if ch.isalnum() else "-" for ch in name.lower()).strip("-").replace("--", "-")


def issuer_coins() -> set[str]:
    """The coin_id each issuer sheet names ("`coin_id` to write): `X`")."""
    out = set()
    for d in ("issuer-packet", "issuer-packet-2"):
        for f in (G / "coders" / d).glob("*.md"):
            if f.name == "README.md":
                continue
            m = re.search(r"`coin_id` to write\): `([^`]+)`", f.read_text(encoding="utf-8"))
            if m:
                out.add(m.group(1))
    return out


def strata() -> dict[str, list[str]]:
    coins = sorted(r["coin_id"] for r in read_csv(G / "coders" / "packet" / "packet.csv"))
    have = issuer_coins()
    return {"with_issuer_sheet": [c for c in coins if c in have], "without": [c for c in coins if c not in have]}


def draw() -> Path:
    prm = yaml.safe_load(CARD.read_text())["parameters"]
    st = strata()
    assert sum(len(v) for v in st.values()) == prm["coins_in_packet"]
    rng = np.random.default_rng(prm["seed"])
    X1.mkdir(parents=True, exist_ok=True)
    out = X1 / "sample.csv"
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["coin_id", "stratum"])
        for name in ("with_issuer_sheet", "without"):
            for c in sorted(rng.choice(st[name], size=prm["strata"][name], replace=False)):
                w.writerow([c, name])
    return out


def norm(v: str) -> str:
    return (v or "").strip().lower()


def origin(settled: str) -> str:
    m = re.search(r"\bS(\d+)\b", settled or "")
    if m:
        return f"S{m.group(1)}"
    if "issuer" in (settled or "") and re.match(r"\s*agreed\s*\|", settled or ""):
        return "agreed (both layers)"
    return "agreed (issuer layer)" if "issuer" in (settled or "") else "agreed (first layer)"


def issuer_sheets() -> dict[str, Path]:
    out = {}
    for d in ("issuer-packet", "issuer-packet-2"):
        for f in (G / "coders" / d).glob("*.md"):
            m = re.search(r"`coin_id` to write\): `([^`]+)`", f.read_text(encoding="utf-8"))
            if m and f.name != "README.md":
                out[m.group(1)] = f
    return out


def m7_extract() -> str:
    text = subprocess.run(["git", "show", f"{M7_AT}:{M7}"], cwd=ROOT, check=True, capture_output=True,
                          text=True).stdout
    parts = re.split(r"(?m)^(?=## \d+\. )", text)
    keep = [p for p in parts if (m := re.match(r"## (\d+)\. ", p)) and int(m.group(1)) in M7_SECTIONS]
    return "# The protocol's sections 3, 9, 14 and 17\n\n" + "\n".join(keep)


OUTPUT_SPEC = """# What you write (this sheet prevails over every other instruction in this folder)

You code each coin of `sheets/` on four lines **at its launch only** (no after-change rows): `redemption`, `limit by
rule`, `limit by institution`, `taken back`; each `yes`, `no` or `cannot be read`, by M0's text as the instructions
print it. Read only the files in this folder: `docs/` holds every frozen file the sheets name, under neutral names
(the sheets and the readings' table say which is which). Open nothing outside this folder, run no command on any
other path, and use no web tool. Begin every shell command with `cd <this folder> &&` (its absolute path, as given
to you), and use no other `cd`, no `..`, no `~` and no `$`; give every file tool an absolute path inside this folder;
run commands by their name (`pdftotext`, `python3`); write any working file under `out/` only. A line no file here prints is `cannot be read`.

Stricter still, and checked on every command: use no shell variable (no `$` at all, so no loops over file names in
the shell); never write two dots in a row anywhere in a command, not even inside a quoted string; put no regular
expression containing a slash in a command. When you need a loop, a regular expression or text cleaning, write a
Python script to a file under `out/` with the file tool and run it by name (`python3 out/name.py doc-52`). Keep every
output short (pipe to `head -c 20000`, or print only what you need), so that nothing is saved outside this folder.

Write one file, `out/codes.csv`, columns exactly:

`coin_id,line,phase,code,who,who_class,source,locator,note`

- `coin_id`: as the sheet writes it. Four rows per coin; `phase` = `launch`.
- `who`: on a redemption `yes`, who may redeem **in the issuer's own words**, never paraphrased; else empty.
- `who_class`: on a redemption `yes`, one of M0's two classes, `any holder` or `verified customers only`; else empty.
- `source`: the neutral file name (`doc-NN...`) or the reading's label; `locator`: the page, section or heading
  (a version date where the file has one). Empty only where the code is `cannot be read`.
- `note`: a quotation of twelve words at most, the reason for `cannot be read`, `late print` (a version dated more
  than 12 months after the launch), or a mechanism outside the four lines.
"""


def scrub(text: str, rename: dict[str, str], folders: dict[str, str]) -> str:
    for old in sorted(rename, key=len, reverse=True):
        text = text.replace(old, rename[old])
        text = text.replace(Path(old).name, rename[old])
    for folder, new in folders.items():
        text = text.replace(f"`{folder}`", f"`{new}`")
    text = re.sub(r"`[^`\n]*(/|\.py|\.csv|\.md)[^`\n]*`",
                  lambda m: m.group(0) if m.group(0).startswith(("`docs/", "`out/", "`sheets/")) else "`(not staged)`",
                  text)
    return re.sub(r"\b(?=[0-9a-f]*[a-f])(?=[0-9a-f]*\d)[0-9a-f]{7,12}\b", "(a commit)", text)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stage(folder: str) -> Path:
    dest = Path(folder).resolve()
    assert not dest.exists() or not any(dest.iterdir()), f"{dest} is not empty"
    assert ROOT not in dest.parents, "the stage lies outside the workshop"
    for sub in ("instructions", "sheets", "docs", "out"):
        (dest / sub).mkdir(parents=True, exist_ok=True)
    sample = [r["coin_id"] for r in read_csv(X1 / "sample.csv")]
    packet = {r["coin_id"]: r for r in read_csv(G / "coders" / "packet" / "packet.csv")}
    isheets = issuer_sheets()
    readme = (G / "coders" / "packet" / "README.md").read_text(encoding="utf-8")
    table = dict(re.findall(r"(?m)^\| ([A-Za-z0-9-]+) \| `([^`]+)` \|", readme))
    sources: list[Path] = []
    labels: set[str] = set()
    for c in sample:
        sheet = (G / "coders" / "packet" / packet[c]["sheet"]).read_text(encoding="utf-8")
        labels |= {lab for lab in table if re.search(rf"\b{re.escape(lab)}\b", sheet)}
        if c in isheets:
            sources += [ROOT / p for p in re.findall(r"(?m)^  - `(data/frame-g/[^`]+)`", isheets[c].read_text())]
    folders = {}
    for lab in sorted(table):
        if lab not in labels:
            folders[table[lab]] = "not staged"
            continue
        dated = sorted((FROZEN / table[lab]).iterdir())
        files = [f for d in dated if d.is_dir() for f in sorted(d.iterdir()) if not f.name.startswith("MANIFEST")]
        sources += files
        folders[table[lab]] = "PENDING:" + lab
    rename, n = {}, 0
    for f in sources:
        rel = str(f.relative_to(ROOT))
        if rel in rename:
            continue
        n += 1
        rename[rel] = f"doc-{n:02d}" + "".join(f.suffixes[-2:] if f.suffix == ".gz" else f.suffixes[-1:])
    for folder, v in list(folders.items()):
        if v.startswith("PENDING:"):
            folders[folder] = ", ".join(new for old, new in rename.items() if f"/{folder}/" in old)
    for rel, new in rename.items():
        shutil.copyfile(ROOT / rel, dest / "docs" / new)
    texts = {"instructions/00-output.md": OUTPUT_SPEC,
             "instructions/01-protocol-extract.md": m7_extract(),
             "instructions/02-packet-readme.md": readme,
             "instructions/03-issuer-readme.md": (G / "coders" / "issuer-packet" / "README.md").read_text(),
             "instructions/04-issuer-readme-2.md": (G / "coders" / "issuer-packet-2" / "README.md").read_text()}
    for c in sample:
        texts[f"sheets/{slug(c)}.md"] = (G / "coders" / "packet" / packet[c]["sheet"]).read_text(encoding="utf-8")
        if c in isheets:
            texts[f"sheets/{slug(c)}-issuer.md"] = isheets[c].read_text(encoding="utf-8")
    for name, text in texts.items():
        (dest / name).write_text(scrub(text, rename, folders), encoding="utf-8")
    files = sorted(p for p in dest.rglob("*") if p.is_file())
    manifest = {"made_by": "code/cs_e_second.py stage", "m7": f"{M7} at {M7_AT}, sections {list(M7_SECTIONS)}",
                "files": {str(p.relative_to(dest)): sha(p) for p in files},
                "rename": rename, "readings_staged": sorted(labels)}
    out = X1 / f"stage-manifest{RUN}.json"
    out.write_text(json.dumps(manifest, indent=1) + "\n", encoding="utf-8")
    print(out, len(files), "files")
    return out


def inside(path: str, dest: str) -> bool:
    return path == dest or path.startswith(dest + "/")


def isolation(transcript: str, folder: str) -> Path:
    prm = yaml.safe_load(CARD.read_text())["parameters"]
    dest = str(Path(folder).resolve())
    stems = {dest, dest.replace("/private/tmp/", "/tmp/", 1)}
    calls, bad = 0, []
    for line in Path(transcript).read_text(encoding="utf-8").splitlines():
        try:
            rec = json.loads(line)
        except ValueError:
            continue
        content = (rec.get("message") or {}).get("content")
        for item in content if isinstance(content, list) else []:
            if not isinstance(item, dict) or item.get("type") != "tool_use":
                continue
            calls += 1
            name, inp = item.get("name"), item.get("input") or {}
            why = []
            if name in ("WebFetch", "WebSearch") or "browser" in str(name).lower():
                why.append("a web tool")
            if name == "Bash":
                cmd = inp.get("command", "")
                lead = re.match(r"\s*cd\s+(['\"]?)([^'\"\s;&]+)\1\s*&&", cmd)
                if not lead or lead.group(2) not in stems:
                    why.append("does not begin cd <stage> &&")
                rest = cmd[lead.end():] if lead else cmd
                if re.search(r"(^|[\s;&|(])cd\s", rest):
                    why.append("another cd")
                if ".." in rest or "~" in rest or "$" in rest:
                    why.append("a parent, home or variable path")
                paths = re.findall(r"(?<![\w.\-])/[^\s'\"|;&)]*", rest)
                rels = re.findall(r"[\w.\-]+(?:/[\w.\-]*)+", rest)
            else:
                paths = [str(v) for k, v in inp.items() if k in ("file_path", "path", "notebook_path") and v]
                if name == "Glob" and str(inp.get("pattern", "")).startswith("/"):
                    paths.append(str(inp["pattern"]))
                rels = []
                why += [f"a relative path {q!r}" for q in paths if not q.startswith("/")]
            why += [f"outside: {q}" for q in paths if q.startswith("/") and not any(inside(q, d) for d in stems)]
            words = [q for q in paths + rels]
            for t in prm["isolation_terms"]:
                if any(t in q.replace(d, "") for q in words for d in stems):
                    why.append(f"the term {t!r} in a path")
            if why:
                bad.append({"tool": name, "why": why, "input": json.dumps(inp)[:300]})
    out = X1 / f"isolation{RUN}.json"
    out.write_text(json.dumps({"tool_calls": calls, "void": bool(bad) or calls == 0, "breaches": bad}, indent=1)
                   + "\n", encoding="utf-8")
    print(out, calls, "calls", len(bad), "breaches")
    return out


def places(*fields: str) -> str:
    items = set()
    for f in fields:
        for part in re.split(r"[|;]", f or ""):
            part = re.sub(r"\bwho:.*$", "", part).strip(" .,")
            if part:
                items.add(part)
    return " ; ".join(sorted(items))


def disagreements(prm: dict) -> tuple[list, list, list, dict, dict]:
    srows = read_csv(X1 / "sample.csv")
    stratum = {r["coin_id"]: r["stratum"] for r in srows}
    settled = {(r["coin_id"], r["line"]): r for r in read_csv(G / "mapping.csv") if r["phase"] == "launch"}
    coder = {(r["coin_id"], r["line"]): r for r in read_csv(X1 / "mapping.csv") if r.get("phase", "launch") == "launch"}
    rename = json.loads((X1 / f"stage-manifest{RUN}.json").read_text())["rename"]
    pairs, rows, missing = [], [], []
    for r in srows:
        c = r["coin_id"]
        for line in prm["lines"]:
            s, x = settled.get((c, line)), coder.get((c, line))
            if s is None or x is None:
                missing.append({"coin_id": c, "line": line, "settled": s is not None, "coder": x is not None})
                continue
            a, b = norm(x["code"]), norm(s["code"])
            pairs.append((a, b, stratum[c]))
            if a != b:
                rows.append({"coin_id": c, "line": line, "coder": a, "settled": b, "stratum": stratum[c],
                             "origin": origin(s.get("settled", "")),
                             "coder_source": x.get("source", ""), "coder_locator": x.get("locator", ""),
                             "settled_source": scrub(s.get("source", ""), rename, {}),
                             "settled_locator": scrub(s.get("locator", ""), rename, {})})
    return pairs, rows, missing, coder, stratum


def blind() -> Path:
    prm = yaml.safe_load(CARD.read_text())["parameters"]
    _, rows, _, _, _ = disagreements(prm)
    rng = np.random.default_rng(BLIND_SEED)
    key, inp = [], []
    for r in rows:
        coder_is = "A" if rng.integers(2) == 0 else "B"
        a, b = (r["coder"], r["settled"]) if coder_is == "A" else (r["settled"], r["coder"])
        key.append({"coin_id": r["coin_id"], "line": r["line"], "coder_is": coder_is})
        inp.append({"coin_id": r["coin_id"], "line": r["line"], "A_code": a, "B_code": b,
                    "places": places(r["coder_source"], r["coder_locator"], r["settled_source"],
                                     r["settled_locator"])})
    for name, data in (("blind-key.csv", key), ("reader-input.csv", inp)):
        with (X1 / name).open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(data[0]) if data else ["coin_id", "line"])
            w.writeheader()
            w.writerows(data)
    print(len(rows), "disagreements")
    return X1 / "blind-key.csv"


def kappa(pairs: list[tuple[str, str]]) -> float | None:
    n = len(pairs)
    if not n:
        return None
    po = sum(a == b for a, b in pairs) / n
    ca, cb = Counter(a for a, _ in pairs), Counter(b for _, b in pairs)
    pe = sum(ca[k] * cb[k] for k in CODES) / n ** 2
    return (po - pe) / (1 - pe) if pe < 1 else None


def compare() -> Path:
    from ft import cards
    cards.require_locked(CARD)
    prm = yaml.safe_load(CARD.read_text())["parameters"]
    iso = json.loads((X1 / f"isolation{RUN}.json").read_text())
    if iso["void"]:
        return cards.write_result(STUDY, CARD, {"void": True, "why": "the coder's isolation failed", "isolation": iso})
    sample = [r["coin_id"] for r in read_csv(X1 / "sample.csv")]
    pairs, rows, missing, coder, stratum = disagreements(prm)
    who_settled = {r["coin_id"]: r["class"] for r in read_csv(G / "coders" / "who-classes.csv")}
    verdicts = {(r["coin_id"], r["line"]): r for r in read_csv(X1 / "readings.csv")}
    blind_ = {(r["coin_id"], r["line"]): r["coder_is"] for r in read_csv(X1 / "blind-key.csv")}
    for r in rows:
        v = verdicts.get((r["coin_id"], r["line"]))
        raw = v["verdict"].strip() if v else "not read"
        side = blind_[(r["coin_id"], r["line"])]
        r["verdict"] = ("coder" if raw == side else "settled") if raw in ("A", "B") else raw
        r["rule_named"] = v.get("rule", "") if v else ""
        r["passage"] = v.get("passage", "") if v else ""
        r["variant_code"] = {"coder": r["coder"], "neither": "cannot be read"}.get(r["verdict"], r["settled"])
    settled_red = {r["coin_id"]: norm(r["code"]) for r in read_csv(G / "mapping.csv")
                   if r["phase"] == "launch" and r["line"] == "redemption"}
    who, who_unsettled = [], []
    for c in sample:
        x = coder.get((c, "redemption"))
        if not (x and norm(x["code"]) == "yes" and settled_red.get(c) == "yes" and c in who_settled):
            continue
        row = {"coin_id": c, "coder": norm(x.get("who_class", "")), "coder_words": x.get("who", ""),
               "settled": norm(who_settled[c])}
        (who_unsettled if row["settled"] == "not settled" else who).append(row)
    invalid = [{"coin_id": k[0], "line": k[1], "code": v["code"]} for k, v in coder.items()
               if norm(v["code"]) not in CODES]
    wrong = [r for r in rows if r["verdict"] in ("coder", "neither") and r["variant_code"] != r["settled"]]
    table = {f"{a} | {b}": n for (a, b, _), n in Counter(pairs).items()}
    by_stratum = {s: {"coin_lines": len(pp), "agreed": sum(a == b for a, b in pp), "kappa": kappa(pp)}
                  for s in ("with_issuer_sheet", "without")
                  for pp in [[(a, b) for a, b, z in pairs if z == s]]}
    payload = {
        "void": False, "isolation": {"tool_calls": iso["tool_calls"], "breaches": 0},
        "coins": len(sample), "coin_lines": len(pairs), "agreed": sum(a == b for a, b, _ in pairs),
        "kappa": kappa([(a, b) for a, b, _ in pairs]), "by_stratum": by_stratum,
        "disagreements_by_origin": dict(Counter(r["origin"] for r in rows)),
        "disagreements_by_stratum": dict(Counter(r["stratum"] for r in rows)),
        "table_coder_by_settled": table, "missing": missing,
        "disagreements": rows, "unread_disagreements": sum(r["verdict"] == "not read" for r in rows),
        "verdicts": dict(Counter(r["verdict"] for r in rows)),
        "settled_wrong_at_document": wrong,
        "who_may_redeem": {"compared": len(who), "agreed": sum(w["coder"] == w["settled"] for w in who), "rows": who,
                           "settled_not_settled": who_unsettled},
        "invalid_coder_codes": invalid,
        "variant_needed": bool(wrong),
        "said": "g1 and g2 (and i1-i4) were two runs of one model (Sonnet); this coder is another model (Opus 5.5)",
    }
    out = cards.write_result(STUDY, CARD, payload)
    print(out)
    return out


if __name__ == "__main__":
    {"draw": draw, "stage": stage, "isolation": isolation, "blind": blind, "compare": compare}[sys.argv[1]](
        *sys.argv[2:])
