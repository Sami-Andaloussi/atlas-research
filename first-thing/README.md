# First Thing: methods and proof

First Thing publishes short studies in economics on
[first-thing-research.com](https://first-thing-research.com): a question readers ask, answered from what economics
already knows, from history's cases and from analyses of our own. The study itself, with its argument, its charts
and its calculators, lives on the site. This folder holds what stands behind it, for the sceptic and the specialist.

The studies follow the discipline set out in [Atlas Research](../README.md): every number pinned to its source
and its date, every protocol fixed before its result, every claim labelled by the kind of evidence behind it. They are
built with their own tools, described below.

## What each study's folder holds

- **`README.md`**, the methods and proof: what each claim rests on, what was fixed before each result, what ran,
  what each result means and what it does not.
- **`results/numbers.json`**, the register of every number and every claim the study prints. Each claim has its
  evidence type: *established* (a documented fact or mechanism, cited at its passage), *cases* (shown in history,
  with sources), *measured* (an analysis of ours) or *judgement* (our reading, said as ours). Each number names the
  script that computed it or the source it is cited from.
- **`cards/`**, the protocol of each analysis of ours, committed before any result on its data existed. A result
  in `results/runs/` names the hash of the card it ran under. Cards are published as locked: only private file paths and internal process notes were edited, and no rule, number or source changed. `REDACTIONS.md` gives the hash of every card and protocol before and after.
- **`code/`**, the scripts that compute every number and draw every figure.
- **`data/`**, a manifest for each dataset: where it was fetched, when, and its hash. Fetched data is not
  republished. A dataset we built ships its values only when they are ours to share, such as our own coding of
  public documents; otherwise its manifest names its sources, with the table and page where they are printed.
  `results/datasets.yaml` lists every dataset the study reads.
- **`WITHHELD.md`**, what the public copy leaves out and why: a file or a value that another publisher's licence
  keeps from republication, or a table transcribed from a printed work. **`REDACTIONS.md`**, where a path on our
  machines or a link to our private project was replaced, and where a quoted passage was shortened.
- **`sources.md`**, the works cited. The register's claims give the page or section each was read at, with the
  passage quoted as a short excerpt.
- **`figures/`**, where a study's folder has them, as published, unless `WITHHELD.md` says otherwise.

## How far a study can be reproduced

Each study's README states its level. For the first studies it is **read the code**: every number and every source
can be traced to its script or its source, but the scripts rely on a shared toolkit that is not published, so they
can be read and checked, not rerun from a folder alone.

## Corrections

A study found wrong is corrected in the open: the change is dated and described in its README and on its page, and
the earlier version stays in this repository's history.

## The studies

<!-- index:start -->
| Study | Title |
|---|---|
| **FT-001** | *published part by part* |
| part 1 — [FT-001-part-1-what-gives-a-money-its-value](FT-001-part-1-what-gives-a-money-its-value/) | What gives a money its value? — methods and proof |
| part 1 — [FT-001-part-1-what-trust-rests-on](FT-001-part-1-what-trust-rests-on/) | Does a money lose its value when its backing goes? — methods and proof — *superseded by [FT-001-part-1-what-gives-a-money-its-value](FT-001-part-1-what-gives-a-money-its-value/)* |
| part 2 — [FT-001-part-2-where-money-comes-from](FT-001-part-2-where-money-comes-from/) | Where money comes from — methods and proof |
| part 2 — [FT-001-part-2-where-printed-money-goes](FT-001-part-2-where-printed-money-goes/) | Does printing money really cause inflation? — methods and proof — *superseded by [FT-001-part-2-where-money-comes-from](FT-001-part-2-where-money-comes-from/)* |
<!-- index:end -->
