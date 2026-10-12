"""The case record's sweep (part 1's map v18, §2 part 2): every read passage on a told case, before the case is written.

For each told case, `notes/case-terms.json` holds a term list written before the sweep — its series-map marks, place,
institutions, people, instruments, years (`terms`) — and the sources its telling cites, each with a pattern for its
author or title (`cited`). The sweep reads the project's notes, harvests, checks and maps, as `/usr/bin/grep -r` would
(gitignored files included), and prints, per case:

- each line naming one of its terms (tier A);
- each line naming a cited source within six lines of one of its terms (tier B).

It refuses (exit 1) a case whose cited source it does not return in tier A or B **from the study folders' notes**
(the registry of passages read, P09): the maps and checks restate each telling, so they would satisfy the rule by
themselves (the map v19 audit measured it). The term list is then widened, or the source's passage recorded in the
notes, before the case is written. It holds the list's recall against the telling's own citations, never the
choice of terms, which the case record says.

    python first-thing/FT-001-part-1-what-gives-a-money-its-value/code/case_sweep.py [CASE ...] [--quiet]
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
STUDY = Path(__file__).resolve().parents[1]
TERMS = STUDY / "notes" / "case-terms.json"
DIRS = [
    "first-thing/FT-001-part-1-what-gives-a-money-its-value/notes",
    "first-thing/FT-001-part-2/notes",
    "an internal note",
]
NEAR = 6
NOTES = tuple(ROOT / d for d in DIRS[:2])


def files() -> list[Path]:
    out = []
    for d in DIRS:
        for p in sorted((ROOT / d).rglob("*")):
            # the term lists and the case record's own lists would satisfy the recall rule by themselves
            if p == TERMS or p.name.startswith("case-record"):
                continue
            if p.is_file() and p.suffix in {".md", ".txt", ".csv", ".yaml", ".json"}:
                out.append(p)
    return out


def sweep(case: dict, corpus: list[tuple[Path, list[str]]]) -> tuple[list, list, set]:
    term = re.compile("|".join(case["terms"]), re.I)
    cited = {name: re.compile(pat, re.I) for name, pat in case["cited"].items()}
    tier_a, tier_b, found = [], [], set()
    for path, lines in corpus:
        near = [i for i, line in enumerate(lines) if term.search(line)]
        in_notes = path.is_relative_to(NOTES[0]) or path.is_relative_to(NOTES[1])
        for i in near:
            tier_a.append((path, i + 1, lines[i]))
            if in_notes:
                found |= {n for n, c in cited.items() if c.search(lines[i])}
        hit = set(near)
        for i, line in enumerate(lines):
            if i in hit:
                continue
            names = {n for n, c in cited.items() if c.search(line)}
            if names and any(abs(i - j) <= NEAR for j in near):
                tier_b.append((path, i + 1, line))
                if in_notes:
                    found |= names
    return tier_a, tier_b, set(cited) - found


def main(argv: list[str]) -> int:
    quiet = "--quiet" in argv
    wanted = [a for a in argv if not a.startswith("--")]
    cases = json.loads(TERMS.read_text(encoding="utf-8"))
    corpus = [(p, p.read_text(encoding="utf-8", errors="replace").splitlines()) for p in files()]
    failed = []
    for name, case in cases.items():
        if wanted and name not in wanted:
            continue
        tier_a, tier_b, missing = sweep(case, corpus)
        print(f"== {name}: {len(tier_a)} lines (A), {len(tier_b)} near (B), missing cited: {sorted(missing) or 'none'}")
        if not quiet:
            for tier, rows in (("A", tier_a), ("B", tier_b)):
                for path, n, line in rows:
                    print(f"  {tier} {path.relative_to(ROOT)}:{n}: {line.strip()[:240]}")
        if missing:
            failed.append(name)
    if failed:
        print("refused: cited sources not returned for " + ", ".join(failed) + "; widen their term lists")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
