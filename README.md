# Atlas Research

Turning discretionary analysis into data.

---

## The idea

A research report is normally a document. Someone reads it, forms an opinion, and once the reading
is over nothing measurable remains: you cannot query it later, compare it to the next one, or ask
what it said before the numbers were revised.

Atlas treats a report as a **data point** instead — dated, sourced, versioned, and handled the way
an economic release is handled. Producing a report is not publishing; it is recording an
observation.

That choice sets the shape of everything else:

**Granularity.** Not one report of two hundred pages, but two hundred reports of one page — one per
country, per sector, per commodity, per company. Small units compose; a large document does not.

**Provenance.** If a report is data, every number in it has to say where it came from, precisely
enough to be re-read.

**Point in time.** Economic data is revised. GDP for 2024 is not the same number in March and in
September. A dataset that overwrites cannot answer what was known at the time, so this one keeps
the date attached.

**A shared vocabulary.** Two reports are only comparable if they classify their subjects the same
way, so the classification layer is part of the system rather than a convention.

The constraints below are consequences of that idea, not extra rigour added on top.

---

## What the system holds to

**A number that cannot be traced is not published.** Every value keeps a pointer to the exact byte
range of the document it was read from. If the document changes, the pointer breaks and the system
refuses.

**Public sources only.** No paid data broker. This narrows what can be claimed — unlisted Swiss
companies do not publish accounts, so Atlas will never hold them — and it means any source used
here can be re-fetched by a reader.

**Three planes are kept apart** in the classification layer: what exists, the question being asked,
and the operational data behind it. A sector is not a company; an instrument is not its underlying.

**Validation can refuse the people building the system.** The build stops when a claim is not
backed — a size ceiling that redirects work instead of being raised, a check that a fix's proof is
reachable by anyone rather than only on the machine that produced it, and a rule that blocks
tooling commits when the product itself has not advanced.

**LLM agents are orchestrated as an engineering method.** Several agents run in parallel on separate
branches, merged through a written inspection procedure. No agent reviews its own work: every fix
goes to a separate agent that did not write it, and a human arbitrates.

---

## How it works

```
   public sources         governed capture        point-in-time store        rendering
 ┌────────────────┐     ┌──────────────────┐     ┌───────────────────┐     ┌──────────────┐
 │  World Bank    │     │  bytes retrieved │     │  values + vintage │     │  a page that │
 │  FRED, BEA     │ ──▶ │  hashed, stored  │ ──▶ │  + provenance     │ ──▶ │  cites its   │
 │  OFS, SNB      │     │  attested        │     │  + anchors        │     │  sources     │
 │  Fedlex, simap │     └──────────────────┘     └───────────────────┘     └──────────────┘
 └────────────────┘              │                         │                      │
                                 ▼                         ▼                      ▼
              ┌──────────────────────────────────────────────────────────────────────┐
              │   validation — 599 modules that refuse what cannot be proven          │
              └──────────────────────────────────────────────────────────────────────┘
```

The renderer runs in a separate process that never held the observations in memory, so a page
cannot contain anything that was not read back from disk.

---

## Status

| Component | State |
|---|---|
| Capture, anchoring, storage, re-read, page rendering | Works end to end |
| Data volume | 7 records in the store. The chain is proven, the corpus is not built |
| Classification layer wired to the report generator | Not yet — the next structural step |
| Scenario layer (mechanisms, second-order consequences) | Designed, not built |
| Product (interface, users, subscription) | None |

Built since 2026-08-07. The build plan holds **170 steps across 14 arcs, 60 of them done**, and
**45 known defects are open and tracked**. The defect count is published on purpose: it stayed
frozen for 24 days while a lot of other work happened, which was the signal that the work was not
going where it was supposed to.

---

## What is in this repository

This is the public window on the project. The implementation is in a private repository.

| Path | What it holds |
|---|---|
| [`examples/`](examples/) | A real captured document, the record derived from it, and a script that re-reads the byte ranges — the provenance claim, checkable in one command. Also a real generated page, unchanged. |
| [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) | The chain layer by layer, and what each one refuses. |
| [`docs/METHOD.md`](docs/METHOD.md) | How the work is split between LLM agents, and the rules that keep them honest. |
| [`docs/PROGRESS.md`](docs/PROGRESS.md) | Measured state, with the numbers quoted from the project's own counters. |
| [`docs/ROADMAP.md`](docs/ROADMAP.md) | The 14 arcs, and what is deliberately deferred. |

---

## Limits

- The corpus is tiny. Seven records is a proof of chain, not a dataset.
- The classification layer and the report generator do not talk to each other yet, so refining the
  classification changes nothing in the output today.
- One document format (HTML) can be captured but not yet anchored, so it is excluded rather than
  half-read.
- Coverage findings for Switzerland and the United States come from an internal study that is not
  published here. Those cannot be verified from this repository, and the page says so rather than
  implying otherwise.

---

Built by Sami Andaloussi. Questions and corrections are welcome — especially "your number is wrong".
