# Architecture

How Atlas is put together, and why each layer exists. Every design choice below was made to answer
one question: **can a reader catch this system being wrong?**

## The chain, layer by layer

### 1. Sources — public only

Public data and public APIs, never a paid data broker. World Bank, FRED, BEA, the Swiss Federal
Statistical Office, the Swiss National Bank, Fedlex, the commercial register, public procurement.

This is a constraint with teeth: it means every figure Atlas publishes can be independently
re-fetched by whoever doubts it. It also means Atlas **cannot** promise things that are not public
— the accounts of an unlisted Swiss company, for instance. Saying so is part of the design.

### 2. Capture — bytes, not strings

A capture retrieves the **actual bytes** from a source and stores them with a hash and a manifest
entry. What is kept is not "GDP was 29 298 013 000 000" but the document that said so.

Two consequences fall out of this:

- A value can always be traced back to a slice of a real document.
- A document that cannot be anchored is **refused rather than silently accepted**. A recent example:
  a PDF entered the system only after it was given an explicit named refusal path
  (`non-text bytes`), because the generic reader could not have honestly handled it. An HTML
  document still lacks its equivalent — and so it is excluded, visibly, instead of being half-read.

### 3. Anchoring — the value equals the slice

An **anchor** binds a value to a byte range in a captured document, such that re-reading the range
reproduces the value. If the document changes, the anchor breaks loudly.

This is what separates "the system says 29.3 trillion" from "here is the sentence, in the document
we captured on this date, that says 29.3 trillion".

### 4. Point-in-time store — what was known, when

Economic series are revised. A store that overwrites is a store that will confidently misreport the
past. Every observation carries the **vintage** it belongs to, so a question can be asked as
*"what did we know on this date"* rather than only *"what is true now"*.

This is also where a subtle class of bug lives, and the project has paid for it repeatedly: any
frozen literal that describes a *population* — a count of records, a set of identifiers — dies the
moment the population moves. Six instances of that single class were found in one night. The
adopted remedy is a shared predicate based on **git traceability** rather than disk presence, so
that a test asks "is this reachable by everyone" instead of "is this on my machine".

### 5. Rendering — in a process that never held the data

The renderer reads the store **in a separate process that never had the observations in memory**.
That is not a performance choice. It is a proof: an output produced this way cannot have carried
over hidden information from the step that built it.

The current page states, in its own text, which of its claims are derived and which are hand-made,
and names the plan item that will make it refuse to run until the selection is derived.

### 6. The Atlas grammar — what makes subjects comparable

Above the data sits the classification layer that gives the project its name. It separates three
planes:

- **the referent** — what exists or happens: an entity, a system, a process, a flow, an instrument;
- **the analytical** — the question asked, the lens, the horizon, the comparator;
- **the operational** — data families, resolutions, cadences, coverage levels.

A sector is not a company. A technology is not an activity. An instrument is not its underlying.
Keeping those apart is what lets two reports on unrelated subjects be read the same way.

**Size:** 25 facet shards, 52 term shards, 5 axes, 196 fixtures, and a relation catalogue that
declares which links between objects are even sayable.

**An honest gap:** the report generator does not consult this layer yet. The grammar is built, the
wiring is not. It is the next structural step, and it is named as such in the
[roadmap](ROADMAP.md).

## The validation layer

**599 modules and 120 test files** exist to stop work from landing. A few of the properties they
enforce, chosen because they are unusual:

| Gate | What it refuses |
|---|---|
| Ceilings | any text file past a size a reader can hold; the ceiling redirects work, it is never raised |
| Anchoring | a tracked document that no anchor can bind |
| Closure | a defect declared fixed whose proof is not reachable by git |
| Coverage | a new module that no inventory mentions |
| Drift | tooling commits that pile up while the product does not advance |
| Duration | a gate run that exceeds its own time budget |

Two design rules apply to all of them:

- **A check that prints is not a gate.** If it does not refuse, it does not count.
- **A gate must be shown to refuse.** A test that has never failed on purpose has not been shown to
  work; sabotage is injected deliberately to confirm each one catches what it claims to catch.

## Repository shape

```
atlas/        the classification grammar — facets, axes, terms, relations
core/         the normative contract and object model
engine/       capture, store and rendering
scripts/      acquisition and orchestration entry points
validation/   599 modules that refuse
plan/         14 arcs, 170 steps — the build itself, versioned
state/        measurements, audits, decisions, provenance manifests
```

`plan/` and `state/` being versioned is deliberate. The build's own history — what was decided,
what was measured, what was refused and why — is part of the artefact, not a side channel.

## What is not built

Named plainly, because a page that only lists what works is not an architecture document:

- no user interface, no accounts, no subscription;
- the grammar and the generator are not connected;
- the scenario layer — mechanisms, second-order consequences — is designed but not implemented;
- the volume of data is small; the plumbing is proven, the corpus is not there.
