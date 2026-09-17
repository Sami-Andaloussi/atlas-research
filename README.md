# Atlas Research

**An economic-intelligence system that shows its work.**

Atlas produces research on countries, sectors, companies and markets for people who need to
understand what is changing around their business — and who cannot spend their evenings sorting
through dozens of sources of uneven quality.

The distinguishing constraint is not the writing. It is that **every fact carries its source, its
date, and its point-in-time status** — and that the system is built to refuse its own output when
it cannot prove it.

> **Status: under active construction.** This page is a window into a working project, not a
> product launch. Section [Where it actually stands](#where-it-actually-stands) says exactly what
> runs today and what does not. Nothing on this page is a claim I cannot back with a measurement.

---

## The problem

A business owner exposed to several countries, a global sector, foreign suppliers or a currency
has a real information problem and no good option:

- **News** is fast and shallow. It tells you what happened, rarely what it means for you, and
  almost never what would have to be true for it to matter.
- **Research subscriptions** are written for institutions, priced for institutions, and assume
  you already know the terrain.
- **Asking a language model** gives you fluent prose with no provenance. You cannot tell which
  sentence came from a real source and which one was invented, and you find out the wrong way.

The gap is not "more information". It is **traceable understanding**: what changed, where the
number comes from, when it was true, what mechanism connects it to you, and what would break the
reasoning.

## What Atlas produces

Three depths, one research base:

| | what it is |
|---|---|
| **Signal** | what changed and what deserves attention |
| **Briefing** | a periodic read tied to your world, with mechanisms and conditional scenarios |
| **Dossier** | a deep read of one country, sector, company or question |

Every output follows the same discipline, and it is written into the system rather than left to
good intentions:

1. the **facts** and where they come from;
2. the **interpretation**, stated as interpretation, with the mechanisms that could explain it;
3. **conditional scenarios** with first- and second-order consequences;
4. the **limits** — what is unknown, and what would invalidate the reasoning.

**What it is not:** not a trading signal, not a recommendation, not a substitute for legal, tax or
accounting advice. Atlas explains a situation; it never tells you what to do with your money.

---

## What makes it different

Most AI-assisted research tools optimise for fluency. Atlas optimises for **falsifiability** — you
should be able to catch it being wrong.

### Every number is anchored to bytes somebody captured

A fact in Atlas is not a string in a database. It is a value tied to a **capture**: the actual
bytes retrieved from a source, stored, hashed, and re-readable. The system can be asked *"show me
the slice of the original document this number came from"* and it will produce it — or refuse.

### The point-in-time discipline

Economic data is revised. GDP for 2024 is not the same number in March and in September, and a
system that silently overwrites the old value will confidently tell you something false about the
past. Atlas treats **"what was known, when"** as a first-class axis. A figure carries the vintage
it belongs to.

### Gates that refuse, including to their author

The repository carries **599 validation modules** and **120 test files** whose job is to stop work
from landing. They are not advisory. Measured examples from a single day of construction:

- a commit was refused because a docstring claimed an operation cost `0.27s` when re-measurement
  showed **38.3s** — the underlying population had grown and the frozen number had not followed;
- a merge was refused because a tracked manifest referenced bytes that had **never been committed
  anywhere** — true on the machine that captured them, false everywhere else;
- a change was refused because it would have been the **4th tooling commit in a row** while the
  product itself had not advanced.

The third one is the point: the system pushes back on its own builder drifting away from the goal.

### Nothing closes on its author's word

Any claim that a defect is fixed goes to an **independent reviewer** that did not write the fix.
**954 audit documents** live in the repository. They regularly demolish work — including work I was
confident in. One recent verdict caught a justification I had fabricated by misreading a failed
command's silence as a result. That finding is recorded in the repository rather than quietly
dropped, because a project that hides its own corrections cannot ask anyone to trust its output.

---

## Where it actually stands

**Honest version, measured 2026-09-16.**

✅ **The full chain runs end to end.** Public API → governed capture → stored bytes with provenance
→ re-read in a *separate process that never held the data in memory* → rendered page. The
separation matters: it proves the output was derived, not remembered.

✅ **The page declares its own limits.** The current output states in writing which of its claims
are hand-made and which are derived, and names the plan item that will force it to refuse to run
until the selection is derived rather than chosen.

⚠️ **It runs on very little data.** Today's output is built from a handful of observations. The
plumbing is proven; the volume is not there yet.

⚠️ **The classification layer and the report engine do not talk to each other yet.** The Atlas
grammar (below) is built; the report generator does not consult it. Wiring the two is the next
structural step.

❌ **Not a product.** No interface, no users, no subscription. This is infrastructure being built
in public view.

### The numbers

| | |
|---|---|
| Commits | **2 395** in 40 days (2026-08-07 → 2026-09-16) |
| Tracked files | **3 347** |
| Python / YAML / Markdown | **138k** / **154k** / **346k** lines |
| Validation modules | **599** |
| Test files | **120** |
| Independent audit documents | **954** |
| Plan | **14 arcs**, 173 items — **63 done**, 18 open, 92 waiting |
| Open blocking defects | **45**, named and tracked |

That last row is deliberate. The count of unresolved defects is published and watched, because a
build that only reports progress is reporting half the truth.

---

## How it is built

```
  public sources          governed capture         point-in-time store        rendering
 ┌────────────────┐     ┌──────────────────┐     ┌───────────────────┐     ┌─────────────┐
 │  World Bank    │     │  bytes retrieved │     │  values + vintage │     │  a page     │
 │  FRED / BEA    │ ──▶ │  hashed, stored  │ ──▶ │  + provenance     │ ──▶ │  that cites │
 │  OFS / SNB     │     │  attested        │     │  + anchors        │     │  its sources│
 │  Fedlex, simap │     └──────────────────┘     └───────────────────┘     └─────────────┘
 └────────────────┘              │                         │                      │
                                 ▼                         ▼                      ▼
                        ┌───────────────────────────────────────────────────────────────┐
                        │  validation: 599 modules that refuse what cannot be proven    │
                        └───────────────────────────────────────────────────────────────┘
```

**Public sources only.** A deliberate constraint, not a limitation of means: Atlas uses public data
and public APIs, never a paid data broker. It changes what can be promised — and it makes every
claim independently checkable by whoever reads it.

**The Atlas grammar** is the layer that makes research on different subjects comparable: 25 facet
shards, 52 term shards, 5 axes, 196 fixtures and a relation catalogue. It answers *"how do you
place, link and compose any target or question without pretending one universal tree exists"*.

More detail: [Architecture](docs/ARCHITECTURE.md) · [Method](docs/METHOD.md) ·
[Progress](docs/PROGRESS.md) · [Roadmap](docs/ROADMAP.md)

---

## Coverage

**Switzerland and the United States first.**

A feasibility study measured how accessible each country's public data actually is — 8 source
categories, 102 URLs checked, 48 measurements taken live. The short version:

- **Switzerland is strong** where it is rarely given credit: company registry (793 459 entities,
  free SPARQL), official gazette (open API, same day), public procurement (next day, with the
  winner and the amount), macro statistics, consolidated law.
- **Switzerland is weak** on private company accounts: unlisted companies do not publish them. This
  is a legal fact, not a technical obstacle, and Atlas will not promise what it cannot source.
- **The United States is not better on that specific point** — Delaware requires no balance sheet.
  The United Kingdom is the global exception.
- **A trap worth knowing:** Swiss official titles are translated into four languages, **the bodies
  of the documents are not**. A naive search silently ignores the French- and Italian-speaking
  regions while appearing to work.

---

## Built with Mnémosyne

Atlas is constructed inside **Mnémosyne**, a personal environment for running large
LLM-driven projects under human oversight — memory, library, delegation to parallel agents, and a
rule set that is enforced by code rather than by intention.

What it contributes, concretely:

- **Parallel construction.** Several agents work on separate branches of the same repository; an
  orchestrator merges them through a written inspection procedure. The 2 395 commits above are the
  output of that arrangement.
- **Producer ≠ verifier, enforced.** Delegation of audits is a rule the tooling checks, not a habit.
- **Accumulated lessons.** Defects found once are written down as classes, not cases, so the same
  mistake is expensive to repeat. Several of the refusals quoted on this page exist because an
  earlier version of the same mistake was paid for.

The point is not that an AI wrote the code. It is that **the process caught its own errors often
enough to be worth trusting** — and that when it did not, the failure is in the record.

---

## About

Built by **Sami Andaloussi**. This repository is a public window on the work; the implementation
lives in a private repository.

Questions, critique and "your number is wrong" are all welcome — the last one especially.
