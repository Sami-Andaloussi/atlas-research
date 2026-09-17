# Atlas Research

**Economic research for business owners. Every number can be traced back to the document it came
from — and to the moment it was true, because economic data gets revised.**

---

Atlas produces research on countries, sectors, companies and markets, for people who need to
understand what is changing around their business and cannot spend their evenings sorting through
dozens of sources of uneven quality.

The hard part is not the writing. It is that **a number in a report is worthless if you cannot
check it**. So Atlas is built the other way round from most research tools: the system stores the
actual bytes it retrieved, ties every published number to a slice of a real document, and refuses
to publish anything it cannot trace.

> **This is an active build, not a product launch.**
> The section [Where it stands](#where-it-stands) lists precisely what runs today and what does
> not. Every number on this page was measured in the source repository on 2026-09-16, using the
> repository's own measuring tools.

---

## The problem

A business owner exposed to several countries, a global sector or a foreign supplier has a real
information problem, and three bad options.

| Option | Why it fails |
|---|---|
| **News** | Fast and shallow. Tells you what happened, rarely what it means for you. |
| **Research subscriptions** | Written for institutions, priced for institutions, and they assume you already know the terrain. |
| **Asking a chatbot** | Fluent prose, no provenance. You cannot tell which sentence came from a real source — and you discover which was invented only when it costs you. |

The gap is not *more information*. It is **traceable understanding**: what changed, where the
number comes from, when it was true, what connects it to you, and what would break the reasoning.

---

## What Atlas produces

Three depths, one research base.

| Format | What it is |
|---|---|
| **Signal** | What changed, and what deserves attention. |
| **Briefing** | A periodic read tied to your world, with mechanisms and conditional scenarios. |
| **Dossier** | A deep read of one country, sector, company or question. |

Every output follows the same four-part discipline, and the system enforces it rather than trusting
the writer to remember:

1. **The facts** — and where they come from.
2. **The interpretation** — stated as interpretation, with the mechanisms that could explain it.
3. **Conditional scenarios** — with first- and second-order consequences.
4. **The limits** — what is unknown, and what would invalidate the reasoning.

**What it is not.** Not a trading signal. Not a recommendation. Not a substitute for legal, tax or
accounting advice. Atlas explains a situation; it never tells you what to do with your money.

---

## What makes it different

Most AI-assisted research tools optimise for fluency. Atlas optimises for **being catchable when it
is wrong**.

### Every number is anchored to bytes somebody captured

A fact here is not a string in a database. It is a value tied to the actual bytes retrieved from a
source — stored, hashed, re-readable. The system can be asked *"show me the slice of the original
document this number came from"*, and it either produces it or refuses.

### Revisions do not rewrite the past

Economic data gets revised. GDP for 2024 is not the same number in March and in September, and a
system that silently overwrites will confidently tell you something false about the past. Atlas
treats **what was known, and when** as a first-class axis.

### The gates refuse, including to the person building the system

The repository carries **599 validation modules** and **120 test files** whose job is to stop work
from landing. They are not advisory. Three real refusals, from a single day of construction:

| What was refused | Why |
|---|---|
| A commit | A code comment claimed an operation cost `0.27s`. Re-measured: **38.3s**. The workload had grown; the number written in the comment had not followed. |
| A merge | A tracked index referenced bytes that had **never been committed anywhere** — true on the machine that captured them, false everywhere else. |
| A change | It would have been the **fourth tooling commit in a row** while the product itself had not advanced. |

**The third one deserves its full ending, because a gate that can never be overruled is a different
claim from the one being made here.** That commit did land, the same day. The owner of the project
judged the rule too rigid and arbitrated against it. But the override was not a bypass: the gate
offers a declared exit that has a price — you must name a real product step that this work unblocks,
and the name is checked against the plan. The exit was used, the named step is in the commit, and
the owner's decision is recorded there in his own words.

That is the intended behaviour. The gate makes drift expensive and visible; a human can still
decide, and the decision leaves a trace.

### Nothing closes on its author's word

Any claim that something is fixed goes to an independent reviewer that did not write the fix.
**954 audit documents** live in the repository, and they regularly demolish work.

This page went through one. It found four genuine errors — including the plan figures below, which
were wrong in an earlier draft of this very README, and a refusal story told without its ending.
Both are corrected above. The audit was also wrong twice, and those findings were checked and
rejected rather than accepted on authority.

---

## Where it stands

| Component | Status |
|---|---|
| **The full chain, end to end** | **Working.** Public API, governed capture, stored bytes with provenance, re-read in a separate process that never held the data, rendered page. |
| **A page that declares its own limits** | **Working.** The output states in writing which of its choices are hand-made, and names the step that will force it to refuse to run until they are derived. |
| **Data volume** | **Thin.** Today's page is built from a handful of observations. The plumbing is proven; the corpus is not there. |
| **Grammar connected to the report engine** | **Not yet.** The classification layer is built; the generator does not consult it. This is the next structural step. |
| **Product** | **No.** No interface, no users, no subscription. This is infrastructure being built in public view. |

### The numbers

| Measure | Value |
|---|---|
| Commits | **2 395** in 40 days (2026-08-07 to 2026-09-16) |
| Tracked files | **3 347** |
| Python / YAML / Markdown | **138k** / **154k** / **346k** lines |
| Validation modules | **599** |
| Test files | **120** |
| Independent audit documents | **954** |
| Build plan | **170 steps**, of which **60 done** |
| Open blocking defects | **45**, named and tracked |

The plan figures come from the repository's own counter, quoted verbatim rather than recomputed:

```
etapes=170  faites=60  ENGAGEES=1  LIBRES=14  en_attente=89  vagues=15
```

The last row of the table is deliberate. The count of unresolved defects is published and watched,
because a build that reports only its progress is reporting half the truth.

---

## How it is built

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

**Public sources only.** A deliberate constraint, not a limitation of means: Atlas uses public data
and public APIs, never a paid data broker. It narrows what can be promised, and it makes every
claim independently checkable by whoever reads it.

**The Atlas grammar** is the layer that makes research on unrelated subjects comparable — 25 facet
shards, 52 term shards, 5 axes, 196 fixtures, and a catalogue of which links between objects can
even be stated. A sector is not a company. A technology is not an activity. An instrument is not
its underlying.

**Read further:** [Architecture](docs/ARCHITECTURE.md) · [Method](docs/METHOD.md) ·
[Progress](docs/PROGRESS.md) · [Roadmap](docs/ROADMAP.md)

---

## Coverage: Switzerland and the United States

An internal feasibility study measured how accessible each country's public data actually is —
8 source categories, 102 URLs checked, 48 measurements taken live on 2026-09-16.

| Finding | Detail |
|---|---|
| **Switzerland is strong** where it is rarely given credit | Company registry (793 459 entities, free SPARQL), official gazette (open API, same day), public procurement (next day, with the winner and the amount), central-bank series (open API, no key required, each series carrying its publication date). |
| **Switzerland is weak** on private company accounts | Unlisted companies do not publish them. A legal fact, not a technical obstacle — and Atlas will not promise what it cannot source. |
| **The United States is no better** on that specific point | Delaware requires no balance sheet. The United Kingdom is the global exception. |
| **The United States is better** on aggregation | One federal macro gateway covers 851 100 series. Switzerland has no equivalent: three separate services must be assembled, one of which publishes spreadsheets rather than an API. |
| **A trap worth knowing** | Swiss official titles are translated into four languages; the bodies of the documents are not. A naive search silently ignores the French- and Italian-speaking regions while appearing to work. |

---

## Built with Mnémosyne

Atlas is constructed inside **Mnémosyne**, a personal environment for running large LLM-driven
projects under human oversight: memory, library, delegation to parallel agents, and a rule set
enforced by code rather than by intention.

What it contributes, concretely:

- **Parallel construction.** Several agents work on separate branches of one repository; an
  orchestrator merges them through a written inspection procedure. The 2 395 commits above came out
  of that arrangement.
- **Producer is never verifier.** Delegating audits is a rule the tooling checks, not a habit.
- **Accumulated lessons.** Defects found once are written down as *classes*, not cases, so the same
  mistake becomes expensive to repeat. Several refusals quoted above exist because an earlier
  version of the same mistake was paid for.

The claim is not that an AI wrote a lot of code quickly. It is that **the process caught its own
errors often enough to be worth trusting** — and that where it did not, the failure is in the
record.

---

## About

Built by **Sami Andaloussi**. This repository is a public window on the work; the implementation
lives in a private repository.

Questions, critique, and "your number is wrong" are all welcome. The last one especially.
