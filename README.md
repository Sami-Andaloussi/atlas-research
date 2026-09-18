# Atlas Research

Economic research where every number stays attached to the document it came from, and to the date
that document was published.

I am **Sami Andaloussi**, an engineering student. Atlas Research is the system I am designing and
building. This repository is the public window on it: what I decided, what runs today, and what
does not work yet. The implementation is in a private repository.

---

## What I designed and decided

This is the part I want to be judged on.

**The core rule: a number that cannot be traced is not published.** Every value in the system keeps
a pointer to the exact byte range of the document it was read from. If the document changes, the
pointer breaks and the system refuses. I chose this constraint first and built the rest around it.

**Point-in-time as a first-class axis.** Economic data gets revised: GDP for 2024 is not the same
number in March and in September. Most systems overwrite. I decided the store would keep *what was
known, and when*, so a past statement stays checkable.

**Public sources only.** No paid data broker. This narrows what the product can promise — Swiss
unlisted companies do not publish accounts, so Atlas will never claim to have them — and it means a
reader can re-fetch any source I used.

**A classification layer above the data.** Research on a country and research on a company should
be readable the same way. I separated three planes: what exists, the question being asked, and the
operational data behind it. A sector is not a company; an instrument is not its underlying.

**Validation that can refuse me.** I wrote the rules so that the build stops when a claim is not
backed: a size ceiling that redirects work instead of being raised, a check that a fix's proof is
reachable by anyone and not just on my machine, and a rule that blocks tooling commits when the
product itself has not advanced. That last one has refused my own work.

**Orchestrating LLM agents as an engineering method.** I run several agents in parallel on separate
branches and merge them through a written inspection procedure. The rule I care about most: an
agent never reviews its own work — every fix goes to a separate agent that did not write it. I
arbitrate the disagreements and I own the decisions. Details in [Method](docs/METHOD.md).

---

## Verify it yourself, in 30 seconds

You do not have to take the previous section on trust. This repository contains a real captured
document, the real store record derived from it, and a script that re-reads the byte ranges.

```bash
python3 examples/verify_anchor.py
```

It reads `examples/worldbank-gdp-usa.json` (1 567 bytes, captured from the World Bank API) and
`examples/anchored-line.json` (the record Atlas stored), then checks that each recorded byte range
still contains the value it claims:

```
offset 246, length 14  ->  '29298013000000'   value
offset 133, length 19  ->  '"GDP (current US$)"'   label
offset 108, length 16  ->  '"NY.GDP.MKTP.CD"'   series
offset 218, length  5  ->  '"USA"'   country
offset 231, length  6  ->  '"2024"'   period
```

Change one character in the captured file and the script fails. That is the whole idea, in a form
small enough to check by hand.

The same record also carries four separate timestamps — when the source published, when Atlas
captured, what the value was known to be at that moment, and the as-of date of the store entry.
That is the point-in-time axis, not as a design claim but as fields you can open.

---

## What runs today

| Component | State |
|---|---|
| Capture, anchoring, storage, re-read, page rendering | Works end to end |
| Rendering isolated from the producer | Works — the renderer runs in a separate process that never held the data |
| Data volume | 7 records in the store. The chain is proven, the corpus is not built |
| Classification layer wired to the report generator | Not yet. This is the next structural step |
| Product (interface, users, subscription) | None |

A real generated page is in [`examples/generated-page.md`](examples/generated-page.md), with an
English walkthrough. It is short and it states its own limits, including the fact that its
selection is currently hand-written and the plan item that will force it to refuse to run until
that is fixed.

---

## Where the project stands

Built since 2026-08-07. The build plan has **170 steps across 14 arcs, 60 of them done**, and
**45 known defects are open and tracked**.

I publish the defect count on purpose. It stayed frozen for 24 days while a lot of other work
happened, which told me the work was not going where I thought.

More detail: [Architecture](docs/ARCHITECTURE.md) · [Method](docs/METHOD.md) ·
[Progress](docs/PROGRESS.md) · [Roadmap](docs/ROADMAP.md)

---

## Limits, short version

- The corpus is tiny. Seven records is a proof of chain, not a product.
- The classification layer and the report generator do not talk to each other yet.
- The scenario layer — mechanisms and second-order consequences — is designed, not built.
- One document format (HTML) can be captured but not yet anchored, so it is excluded rather than
  half-read.
- Coverage findings for Switzerland and the United States come from an internal study that is not
  published here. You cannot verify those from this repository, and I would rather say so than
  imply otherwise.

---

## Contact

Built by Sami Andaloussi. Questions and corrections are welcome — especially "your number is wrong".
