# Progress — measured, not estimated

**Snapshot date: 2026-09-16.** Every figure here is read from the repository, not recalled.
Where something is unknown or unbuilt, this page says so.

## The build in numbers

| | |
|---|---|
| First commit | 2026-08-07 |
| Latest commit | 2026-09-16 |
| Commits | **2 395** in 40 days |
| Tracked files | **3 347** |
| Python | **138 012** lines |
| YAML | **154 243** lines |
| Markdown | **345 698** lines |
| Validation modules | **599** |
| Test files | **120** |
| Audit documents | **954** |

The Markdown figure is not padding. `plan/` and `state/` — the build's own reasoning, measurements
and refusals — are versioned alongside the code, because the record of *why* something was accepted
is part of what makes it checkable later.

## Plan

**173 items across 14 arcs — 63 done, 18 open, 92 waiting.** Per-arc breakdown in the
[roadmap](ROADMAP.md).

## The number that actually matters

```
closure_mix = addressed_by_design:6  closed:25  open_accepted:23  open_blocking:45
```

**45 blocking defects remain open, named and tracked.**

This counter is published on purpose, and it is watched more closely than the commit count. A build
that reports only its progress is reporting half the truth. Two things it has taught:

- It sat frozen at 44 for **24 days and 1 702 commits**. A great deal of work happened; none of it
  closed a defect. That is exactly the kind of drift a progress bar would have hidden.
- Closing one defect honestly opened two more, because the fix revealed adjacent problems that had
  been invisible. The counter went *up*. That is the counter working.

## What runs today

✅ **The full chain, end to end.** Public API → governed capture with hashing and attestation →
point-in-time store with provenance and anchors → re-read in a separate process that never held the
data → rendered page citing its sources.

✅ **A first binary document under governance.** A PDF from the BEA entered the system through an
attested capture — with a *named* refusal path for non-text bytes rather than a generic error.

✅ **The renderer declares its own limits in writing**, including which of its choices are hand-made
and the plan item that will force it to refuse to run until they are derived.

## What does not run

⚠️ **Volume.** Today's page is built from a handful of observations. The plumbing is proven; the
corpus is not there.

⚠️ **The grammar and the generator are not connected.** The classification layer is built; the
report engine does not consult it. Until that is wired, refining the grammar changes nothing in the
output.

⚠️ **One format is captured but cannot be carried.** An HTML document referenced by a tracked
manifest cannot itself be tracked, because a tracked document must be anchorable and HTML has no
named refusal path yet. Visible, named, not yet built.

⚠️ **One remedy, wired once.** The shared fix for the "frozen literal describing a moving
population" class is implemented and applied at a single site out of six. The rest are known and
assigned.

❌ **No product.** No interface, no users, no subscription, no pricing in force.

## Recent milestone

**2026-09-16 — the green became reproducible.**

Until that date the repository passed its full validation on the machine it was built on and would
have failed on a clean checkout elsewhere. The cause was a class of defect where a frozen value
described a population that differs between machines *at the same instant*. Six instances were
found in one night by three agents working independently.

The remedy — a shared predicate based on git traceability rather than disk presence — reached the
main branch through a merge of 16 commits and 62 files. The merge tree was predicted by an
independent inspection **before any write**, and the real merge produced the identical hash.

It took four gate runs to land. The first three were refused for: an oversized document that a
filesystem-scanning gate judged even though nobody had versioned it; a count frozen at a value only
true on one disk; and an anchoring rule that correctly rejected a document format the system cannot
yet carry.

All three refusals were correct.
