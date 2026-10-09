"""FT-001 M0's lock, and the check of the case line (FT-001-M0-rules.md, sections 3 and 4).

Every coding mission of FT-001 (M2-M9) calls :func:`require_locked` before it codes anything: the rules,
``FT-001-M0-rules.md`` and its twin ``FT-001-M0-rules.yaml``, must both be committed and unchanged since,
and the pair's hash (:func:`sha256`, over both files) is written into each coded list (the column
``rules_sha256``) and its manifest. The commit order is the lock, as a card's (BLUEPRINT §5 c): a list
whose rules hash is not the committed pair's is refused. Both files are hashed because a rule stated only
in the prose would otherwise change without the hash changing (M0 v1's audit, O16).

:func:`line_problems` is the barrier M0 section 3 promises: a case whose entry is on or after its
outcome, or a response dated before the entry, is refused unless the case is marked *already under way*
or *apart* (an apart line is never counted); a matching measure whose date ends after the entry's is
refused; a counted line whose onset (frame b) is not after its entry is refused (M0 v3's audit, O6); a
date that cannot be read is reported, never raised. Dates are ``YYYY``, ``YYYY-MM`` or ``YYYY-MM-DD``; two dates of different precision are compared
as intervals, and an overlap counts against the case (an entry year that holds its outcome's month is
"on", not "before"; an annual measure for a monthly entry runs past it).

:func:`order_problems` checks the commit order M0 section 3 promises (M0 v2's audit, M13): a coded list
first committed with or before the rules whose hash its lines name is refused, and so is a list first
committed with or before a list it follows (the acts before any outcome). Which lists follow which is
declared in the rules' twin (``case_line.follows``) and read by :func:`list_problems` itself, so a check
run without a flag cannot skip it (M0 v3's audit, M2). What no code can check: that nobody looked at an
outcome before coding the acts.

Run from the workshop's root with the toolkit's interpreter: ``toolkit/bin/ftpy
bank/maps/FT-001/missions/code/m0.py <series.csv> [--after <series.csv> ...]`` checks a coded list.
"""

from __future__ import annotations

import calendar
import csv
import hashlib
import subprocess
import sys
from datetime import date
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
RULES = HERE.parent / "FT-001-M0-rules.yaml"
PROSE = HERE.parent / "FT-001-M0-rules.md"
LOCKED = (PROSE, RULES)


class NotLocked(RuntimeError):
    pass


def rules() -> dict:
    return yaml.safe_load(RULES.read_text())


def sha256(paths: tuple[Path, ...] = LOCKED) -> str:
    """One hash over the rules' files, in a fixed order, each preceded by its name."""
    digest = hashlib.sha256()
    for path in paths:
        digest.update(path.name.encode() + b"\n")
        digest.update(path.read_bytes())
    return digest.hexdigest()


def _git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=RULES.parent, capture_output=True, text=True)


def require_locked(paths: tuple[Path, ...] = LOCKED) -> str:
    """The rules' hash, if every file is committed and unchanged since; refuses otherwise."""
    top = _git("rev-parse", "--show-toplevel").stdout.strip()
    for path in paths:
        rel = path.resolve().relative_to(Path(top).resolve()).as_posix()
        if subprocess.run(["git", "ls-files", "--error-unmatch", rel], cwd=top,
                          capture_output=True).returncode != 0:
            raise NotLocked(f"{rel} is not committed: commit the rules before coding any case")
        if subprocess.run(["git", "diff", "--quiet", "HEAD", "--", rel], cwd=top).returncode != 0:
            raise NotLocked(f"{rel} changed since its commit: a changed rule is a new version, committed first")
    return sha256(paths)


def _interval(text: str) -> tuple[date, date]:
    parts = [int(p) for p in text.strip().split("-")]
    if len(parts) == 1:
        return date(parts[0], 1, 1), date(parts[0], 12, 31)
    if len(parts) == 2:
        last = calendar.monthrange(parts[0], parts[1])[1]
        return date(parts[0], parts[1], 1), date(parts[0], parts[1], last)
    if len(parts) == 3:
        d = date(*parts)
        return d, d
    raise ValueError(f"not a date: {text!r}")


def _before(a: str, b: str) -> bool:
    """True only if a ends strictly before b starts."""
    return _interval(a)[1] < _interval(b)[0]


def _ends_after(a: str, b: str) -> bool:
    """True if a's span runs past the end of b's (an annual date runs past a month of the same year)."""
    return _interval(a)[1] > _interval(b)[1]


REQUIRED = ("money", "frame", "entry_date", "status", "source", "locator", "coder", "rules_sha256")


def line_problems(row: dict, rules_sha: str, statuses: tuple[str, ...] | None = None) -> list[str]:
    """What is wrong with one case line; empty when it passes."""
    if statuses is None:
        statuses = tuple(rules()["case_line"]["statuses"])
    found = [f"empty {f!r}" for f in REQUIRED if not str(row.get(f, "")).strip()]
    if found:
        return found
    status = row["status"].strip()
    if status not in statuses:
        found.append(f"status {status!r} is not one of {list(statuses)}")
    if row["rules_sha256"].strip() != rules_sha:
        found.append("rules_sha256 is not the committed rules' hash")
    exempt = status in ("already under way", "apart")
    entry = row["entry_date"].strip()
    try:
        _interval(entry)
    except ValueError as exc:
        return [*found, str(exc)]
    for field in ("outcome_date", "entry_measure_date", "onset_date"):
        value = str(row.get(field, "")).strip()
        if value:
            try:
                _interval(value)
            except ValueError as exc:
                found.append(f"{field} {value!r} cannot be read ({exc})")
                row = {**row, field: ""}
    outcome = str(row.get("outcome_date", "")).strip()
    if outcome:
        if not _before(entry, outcome) and not exempt:
            found.append(f"entry {entry} is not before its outcome {outcome}: mark it 'already under way'")
    onset = str(row.get("onset_date", "")).strip()
    if onset and status == "counted" and not _before(entry, onset):
        found.append(f"entry {entry} is not before its onset {onset}: mark it 'already under way'")
    measure = str(row.get("entry_measure_date", "")).strip()
    if measure and _ends_after(measure, entry):
        found.append(f"the matching measure ({measure}) runs past the entry ({entry})")
    for item in str(row.get("responses", "")).split(";"):
        item = item.strip()
        if not item:
            continue
        kind, _, when = item.rpartition(":")
        if not kind or not when.strip():
            found.append(f"response {item!r} is not 'type:date'")
            continue
        try:
            _interval(when.strip())
        except ValueError as exc:
            found.append(f"response {item!r} has a date that cannot be read ({exc})")
            continue
        if _before(when.strip(), entry) and not exempt:
            found.append(f"response {item!r} is dated before the entry {entry}: mark it 'already under way'")
    return found


def _run(top: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=top, capture_output=True)


def _top(path: Path) -> Path:
    done = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=path.parent, capture_output=True, text=True)
    return Path(done.stdout.strip()).resolve()


def _first_commit(top: Path, rel: str) -> str | None:
    added = _run(top, "log", "--diff-filter=A", "--format=%H", "--", rel).stdout.decode().split()
    return added[-1] if added else None


def _strictly_before(top: Path, earlier: str, later: str) -> bool:
    return earlier != later and _run(top, "merge-base", "--is-ancestor", earlier, later).returncode == 0


def _pair_hash_at(top: Path, commit: str, rels: list[str]) -> str | None:
    digest = hashlib.sha256()
    for rel in rels:
        shown = _run(top, "show", f"{commit}:{rel}")
        if shown.returncode != 0:
            return None
        digest.update(Path(rel).name.encode() + b"\n")
        digest.update(shown.stdout)
    return digest.hexdigest()


def order_problems(path: str | Path, after: tuple[str | Path, ...] = (),
                   locked: tuple[Path, ...] = LOCKED) -> list[str]:
    """The commit order of a coded list: after the rules its lines name, and after every list it follows.

    A list not yet committed passes the first test by construction (:func:`require_locked` has run), but
    each list it follows must already be committed."""
    path = Path(path).resolve()
    top = _top(path)
    rel = path.relative_to(top).as_posix()
    first = _first_commit(top, rel)
    found: list[str] = []
    rules_rels = [Path(p).resolve().relative_to(top).as_posix() for p in locked]
    if first is not None:
        with open(path, newline="") as handle:
            hashes = {row.get("rules_sha256", "").strip() for row in csv.DictReader(handle)} - {""}
        commits = _run(top, "log", "--format=%H", "--", *rules_rels).stdout.decode().split()
        for wanted in sorted(hashes):
            locked_at = next((c for c in reversed(commits) if _pair_hash_at(top, c, rules_rels) == wanted), None)
            if locked_at is None:
                found.append(f"{rel}: the rules at hash {wanted[:12]} were never committed")
            elif not _strictly_before(top, locked_at, first):
                found.append(f"{rel}: first committed with or before its rules ({wanted[:12]}): the lock is broken")
    for other in after:
        other_rel = Path(other).resolve().relative_to(top).as_posix()
        other_first = _first_commit(top, other_rel)
        if other_first is None:
            found.append(f"{rel}: {other_rel}, which it follows, is not committed")
        elif first is not None and not _strictly_before(top, other_first, first):
            found.append(f"{rel}: first committed with or before {other_rel}, which it follows")
    return found


def declared_follows(path: str | Path, twin: dict | None = None) -> tuple[Path, ...]:
    """The lists a coded list must follow, as the twin declares them by folder (``ft001-<frame>``)."""
    path = Path(path).resolve()
    follows = ((twin if twin is not None else rules()).get("case_line") or {}).get("follows") or {}
    names = follows.get(path.parent.name, [])
    return tuple(path.parent.parent / name / "series.csv" for name in names)


def list_problems(path: str | Path, after: tuple[str | Path, ...] = ()) -> list[str]:
    """Every problem of a coded list, each with its row number (the header is row 1), then its order."""
    sha = require_locked()
    twin = rules()
    statuses = tuple(twin["case_line"]["statuses"])
    found = []
    with open(path, newline="") as handle:
        for i, row in enumerate(csv.DictReader(handle), start=2):
            found += [f"row {i}: {p}" for p in line_problems(row, sha, statuses)]
    follows = tuple(dict.fromkeys([*declared_follows(path, twin), *map(Path, after)]))
    return found + order_problems(path, follows)


if __name__ == "__main__":
    args = sys.argv[1:]
    follows = tuple(args[i + 1] for i, a in enumerate(args) if a == "--after")
    target = next(a for i, a in enumerate(args) if a != "--after" and (i == 0 or args[i - 1] != "--after"))
    problems = list_problems(target, follows)
    print("\n".join(problems) if problems else "ok")
    sys.exit(1 if problems else 0)
