# Roadmap

The build is organised into **14 arcs** holding **173 items**. An item is not a ticket: it names a
property the system must hold, the condition that proves it holds, and what it unblocks. An arc
closes when every item in it has passed an independent review.

**Measured 2026-09-16.** These numbers are read from the plan table, not estimated.

| Arc | What it establishes | Done | Open | Waiting |
|---|---|---|---|---|
| **00** Harness foundations | the rules the build itself obeys | — | — | — |
| **01** Production floor | the contract, the object model, the base types | **9/9** ✅ | 0 | 0 |
| **02** Extensible harness | adding a capability without editing the core | 7/11 | 3 | 1 |
| **03** Capture | retrieving bytes from a source, under governance | 8/20 | 1 | 11 |
| **04** Anchored observation | a value tied to the slice of document it came from | 3/16 | 2 | 11 |
| **05** Point-in-time store | what was known, when — and surviving revisions | 2/15 | 2 | 11 |
| **06** Grid & daily report | selecting from the store and rendering a page | 8/24 | 2 | 14 |
| **07** Algorithmic analysis | computations over the store, declared and reproducible | 3/10 | 2 | 5 |
| **08** Bench & algorithm map | comparing methods rather than asserting one | 0/11 | 0 | 11 |
| **09** Manifest & rendering | the output as a contract object, not a print statement | 0/13 | 0 | 13 |
| **10** Scheduling & batching | producing continuously instead of on demand | 4/15 | 0 | 11 |
| **11** Slot catalogue | the pluggable surface — where theories attach | 0/3 | 1 | 2 |
| **12** Generation engine | assembling a full report from the pieces | 1/1 ✅ | 0 | 0 |
| **13** Library bridge | connecting to the accumulated knowledge base | 1/1 ✅ | 0 | 0 |

**Total: 63 done · 18 open · 92 waiting.**

## How to read this honestly

**The early arcs are the deep ones.** Arcs 03 to 06 — capture, anchoring, point-in-time, rendering —
carry 75 of the 173 items. That is where correctness is decided, and it is where the work is.

**Arcs 12 and 13 show 1/1 and look finished. They are not.** They hold a single foundational item
each; their real weight arrives once arcs 08 and 09 land. A progress bar would be lying here, which
is why this table shows counts rather than percentages.

**Arcs 08 and 09 are at zero and that is the real state.** The bench that compares analytical
methods, and the rendering contract that turns a page into a checkable object, have not started.

## What comes next, in order

1. **Wire the report generator to the Atlas grammar.** Today the classification layer is built and
   the generator does not consult it — so refining the grammar changes nothing downstream. This is
   the structural gap, and it blocks the whole "add a theory, watch the report change" premise.
2. **Derive the selection instead of choosing it.** The current renderer states in writing that its
   selection is hand-made, and names the item that will make it *refuse to run* until derived.
3. **Widen the sources.** Swiss public procurement first — next-day publication, with the winner
   and the amount, which is directly actionable for the intended reader.
4. **Close the open defect count.** 45 blocking defects are named and tracked. That number, not
   the commit count, is the measure of progress.

## The open question being deliberately deferred

The product promise commits to *conditional scenarios with second-order consequences*. That is not
something you bolt onto a store of anchored numbers — it needs the engine to carry mechanisms and
relations, not only values. The relation catalogue exists; the path from it to a rendered scenario
is arc 08 and arc 11, and it is honestly not built yet.

Deferring it is a choice, not an oversight: the discipline of provenance has to hold before the
reasoning layer is worth building on top of it.
