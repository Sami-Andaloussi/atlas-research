# Progress — measured, not estimated

Snapshot: **2026-09-16**.

Every figure here is read from the repository, not recalled. Where something is unknown or unbuilt,
this page says so.

---

## The build in numbers

| Measure | Value |
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

The Markdown figure is not padding. The build's own reasoning, measurements and refusals are
versioned alongside the code, because the record of *why* something was accepted is part of what
makes it checkable later.

**Plan:** 14 arcs. The repository's own counter, quoted verbatim rather than recomputed:

```
etapes=170  faites=60  ENGAGEES=1  LIBRES=14  en_attente=89  vagues=15
```

**170 steps, 60 done.** Per-arc breakdown in the [roadmap](ROADMAP.md).

---

## The number that actually matters

```
closure_mix = addressed_by_design:6   closed:25   open_accepted:23   open_blocking:45
```

**45 blocking defects remain open, named and tracked.**

This counter is published on purpose, and watched more closely than the commit count. Two things it
has taught:

**It sat frozen at 44 for 24 days and 1 702 commits.**
A great deal of work happened; none of it closed a defect. That is exactly the kind of drift a
progress bar would have hidden.

**Closing one defect honestly opened two more.**
The fix revealed adjacent problems that had been invisible, so the counter went *up*. That is the
counter working.

---

## What runs today

**The full chain, end to end.**
Public API, then governed capture with hashing and attestation, then a point-in-time store with
provenance and anchors, then a re-read in a separate process that never held the data, then a
rendered page citing its sources. The process separation is the proof: an output produced this way
cannot have carried over hidden information from the step that built it.

**A first binary document under governance.**
A PDF from the US Bureau of Economic Analysis entered the system through an attested capture, with
a *named* refusal path for non-text bytes rather than a generic error.

**A renderer that declares its own limits in writing.**
Including which of its choices are hand-made, and the plan item that will force it to refuse to run
until they are derived.

---

## What does not run

**Volume is thin.**
Today's page is built from a handful of observations. The plumbing is proven; the corpus is not
there.

**The grammar and the generator are not connected.**
The classification layer is built; the report engine does not consult it. Until that is wired,
refining the grammar changes nothing in the output.

**One format is captured but cannot be carried.**
An HTML document referenced by a tracked index cannot itself be tracked, because a tracked document
must be anchorable and HTML has no named refusal path yet. Visible, named, not yet built.

**One remedy, wired once.**
The shared fix for the *frozen literal describing a moving population* class is implemented and
applied at one site out of six. The rest are known and assigned.

**No product.**
No interface, no users, no subscription, no pricing in force.

---

## Recent milestone — 2026-09-16

**The green became reproducible.**

Until that date the repository passed its full validation on the machine it was built on, and would
have failed on a clean checkout elsewhere. The cause was a class of defect where a frozen value
describes a population that differs between machines *at the same instant*. Six instances were
found in one night by three agents working independently.

The remedy — a shared predicate based on version-control traceability rather than disk presence —
reached the main branch through a merge of 16 commits and 62 files. An independent inspection
predicted the merged tree's hash **before any write**; the real merge produced the identical hash,
so what landed was provably what had been inspected.

It took four gate runs to land. The first three were refused for:

| Refusal | Cause |
|---|---|
| Oversized document | A filesystem-scanning gate judged a file nobody had versioned. |
| Frozen count | A value only ever true on one disk. |
| Anchoring rule | It correctly rejected a document format the system cannot yet carry. |

All three refusals were correct.
