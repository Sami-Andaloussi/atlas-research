# Roadmap

The build is organised into **14 arcs**. The repository's own counter gives the authoritative
totals, quoted verbatim rather than recomputed:

```
etapes=170  faites=60  ENGAGEES=1  LIBRES=14  en_attente=89  vagues=15
```

The counter is written in French, as the rest of the private repository is. In English:
**170 steps, 60 done, 1 in progress, 14 ready to start, 89 waiting on a dependency, 15 not yet
specified precisely enough to start.**

An item is not a ticket. It names a property the system must hold, the condition that proves it
holds, and what it unblocks. An arc closes when every item in it has passed an independent review.

Measured in the source repository on **2026-09-16**.

> **A note on the table below, because two counts would otherwise disagree.** It lists the items
> carrying a numbered `A##-` identifier — **149 of the 170 steps, 46 of the 60 done**. The
> remainder are foundation items that do not carry that identifier, including all of arc 00. The
> authoritative totals are the counter above; the table is a per-arc breakdown of the numbered
> subset, and every cell in it was independently verified.

---

## The 14 arcs

| Arc | What it establishes | Done | Open | Waiting |
|---|---|:--:|:--:|:--:|
| **00** — Harness foundations | The rules the build itself obeys | — | — | — |
| **01** — Production floor | The contract, the object model, the base types | **9 / 9** | 0 | 0 |
| **02** — Extensible harness | Adding a capability without editing the core | 7 / 11 | 3 | 1 |
| **03** — Capture | Retrieving bytes from a source, under governance | 8 / 20 | 1 | 11 |
| **04** — Anchored observation | A value tied to the slice of document it came from | 3 / 16 | 2 | 11 |
| **05** — Point-in-time store | What was known, when — and surviving revisions | 2 / 15 | 2 | 11 |
| **06** — Grid and daily report | Selecting from the store, rendering a page | 8 / 24 | 2 | 14 |
| **07** — Algorithmic analysis | Computations over the store, declared and reproducible | 3 / 10 | 2 | 5 |
| **08** — Bench and algorithm map | Comparing methods rather than asserting one | 0 / 11 | 0 | 11 |
| **09** — Manifest and rendering | The output as a contract object, not a print statement | 0 / 13 | 0 | 13 |
| **10** — Scheduling and batching | Producing continuously instead of on demand | 4 / 15 | 0 | 11 |
| **11** — Slot catalogue | The pluggable surface, where theories attach | 0 / 3 | 1 | 2 |
| **12** — Generation engine | Assembling a full report from the pieces | **1 / 1** | 0 | 0 |
| **13** — Library bridge | Connecting to the accumulated knowledge base | **1 / 1** | 0 | 0 |

**Subtotal of this table — 46 done, 13 open, 90 waiting, across 149 numbered items.**
Authoritative totals: **170 steps, 60 done** (see the counter at the top).

---

## How to read this honestly

**The early arcs are the deep ones.**
Arcs 03 to 06 — capture, anchoring, point-in-time, rendering — carry 75 of the 149 numbered items.
That is where correctness is decided, and that is where the work is.

**Arcs 12 and 13 show 1 / 1 and look finished. They are not.**
They hold a single foundational item each. Their real weight arrives once arcs 08 and 09 land. A
percentage bar would be lying here, which is why this table shows counts.

**Arcs 08 and 09 sit at zero, and that is the true state.**
The bench that compares analytical methods, and the rendering contract that turns a page into a
checkable object, have not started.

---

## What comes next, in order

**1. Wire the report generator to the Atlas grammar.**
The classification layer is built and the generator does not consult it, so refining the grammar
changes nothing downstream. This is the structural gap, and it blocks the whole premise of *add a
theory, watch the report change*.

**2. Derive the selection instead of choosing it.**
The current renderer states in writing that its selection is hand-made, and names the item that
will make it refuse to run until derived.

**3. Widen the sources.**
Swiss public procurement first — published next day, with the winner and the amount named.

**4. Bring down the open defect count.**
45 blocking defects are named and tracked. That number, not the commit count, is the measure of
progress.

---

## The question being deliberately deferred

The design commits to *conditional scenarios with second-order consequences*. That does not
attach to a store of anchored numbers — it requires the engine to carry mechanisms and
relations, not only values.

The relation catalogue exists. The path from it to a rendered scenario is arcs 08 and 11, and it is
honestly not built.

Deferring it is a choice, not an oversight: the discipline of provenance has to hold before a
reasoning layer is worth building on top of it.
