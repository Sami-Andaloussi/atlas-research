[← L5](L5-scenarios-score.md) · [Up: Blueprint](README.md)

# L6 — Outputs

## TL;DR

A report is a view of stored rows: assembled word for word from pre-written bricks, every number dated and sourced, every scenario with what would invalidate it.
Because the report is data, two reports can be compared line by line, and a past report can be replayed on revised data to see what the revisions alone would have changed.
The same rows feed a point-in-time export for quantitative research, which states the date from which the analysis may be tested.

## Purpose

Give people and programs **projections of the same store**, none of which can add, alter or
reword anything stored. A renderer selects and lays out; it has no authority of its own.

**Success looks like:**
- Every sentence on a page is a stored brick with its holes filled from stored values.
- Two reports on the same subject can be compared automatically, and the comparison says *why*
  each difference arose.
- The export can be loaded by a backtest without any risk of seeing data from after its dates.

## The report

- **Assembled, not written.** The page is built by code from the analysis rows and the card's text
  bricks. No sentence comes from anywhere else. A quotation is a typed slot of a brick, filled with
  the text its anchor re-reads from the captured document.
- **Two formats.** A short note at each important release, and a longer study.
- **Every number dated and sourced**: the series, its publisher, the period, the vintage, and a link
  back to the captured document.
- **Every reading names its lens**, and where several lenses read the situation, each appears with
  what it would expect.
- **Every scenario shows its trigger, its invalidation, its horizon and its judgement date.**
- **Its coverage is printed**: how much of the page was decided by rules, by menu choices, and what
  was left uncovered.
- **Verified, then rendered.** A verifier re-reads every anchor the page will use and signs the
  list; the renderer reads stored rows only, in a separate step that never held the raw
  observations, and refuses any value the verifier did not sign. A page cannot carry anything the
  store does not hold.
- **Not investment advice.** A scenario is an analysis, never an order or a recommendation.
  Publishing is a human decision, never an automatism.

## The report as data

Each report is a manifest: the subject, the date, the card versions, and the identifiers of every
row it shows. That turns three questions that are hard to ask of a document into queries.

### Compare one report with the next

Between two reports on the same subject, every difference is attributed to its causes, taken in a
fixed order: revised data, then new data, then a card change, then a menu pick. Each step is a
counterfactual run that changes one input, reuses the stored model responses wherever its inputs
are unchanged, and is stored with the mode `counterfactual`. A difference can have several causes:

| Cause | Example |
|---|---|
| New data | A new CPI release moved core inflation's three-month pace. |
| Revised data | The previous month's payrolls were revised down. |
| A situation changed | Core PCE crossed half a point above 2 %. |
| A lens reading changed | The rule-based stance moved from neutral to restrictive. |
| A menu pick changed | The tone moved from calm to vigilant. |
| A card changed | The inflation card moved from one version to the next. |
| A scenario moved | A branch was triggered, invalidated or judged. |

A reader sees not only *what* the reading is now, but whether it moved because the world moved,
because the data were revised, or because the method changed.

### Confront a report with the revisions

A past report is replayed with its card versions held fixed, on a later vintage of the same data.
Menu picks are not asked again, since the model now knows how things turned out: the original pick
is reused where its option is still offered, and the replay abstains where it is not. The
difference shows exactly which readings the revisions alone would have changed: a situation that
held on first-release data and fails on revised data is a reading that was right on its day, or
wrong for reasons nobody could see. The best subjects for it are the most revised: GDP, payrolls,
PCE prices, and the seasonal factors behind every monthly pace. Replay rows are stored with the
mode `replay` and never count as analysis.

### Query across reports

Because every reading is a row, questions across reports are ordinary queries. For example: every
report in which core inflation was read as above target while the policy stance was read as
restrictive; every scenario of a given lens judged invalidated within six months; how often a
reading made on first releases survived the revisions.

## The point-in-time export

For quantitative research, the export carries:

- **the facts**, each with its period, vintage, release stage and four instants, and the flag that
  marks history from before a source's real-time record;
- **the analysis atoms** of live runs only, each with its card version, lens, decision kind, claim
  kind and run log;
- **the scenarios and their states**, tagged at birth;
- **the card versions**, with their acceptance dates.

Every record carries the instant it became available: a fact when it was knowable, a row when it was
produced, a scenario when it was registered, a state when it was judged. The export is partitioned
by that instant and shipped with a reader, `as_of(t)`, which applies the same rule as the store's
read: nothing available after `t`. A backtest that goes through the reader cannot see an analysis
before its production date, a verdict before its judgement, or a card before its acceptance.

## Interfaces

| Direction | Artefact | From / to |
|---|---|---|
| in | Analysis rows, coverage | [L4](L4-analysis.md) |
| in | Text bricks, card versions | [L3](L3-subject-cards.md) |
| in | Scenario registry and verdicts | [L5](L5-scenarios-score.md) |
| in | Captured documents, for citations | [L1](L1-facts.md) |
| out | Reports: short note, study | Readers |
| out | Report manifests, comparisons, revision replays | Readers, the workshop |
| out | Point-in-time export | Quantitative research |

## Gates

**Entry.** The analysis store holds a full run for the subject, with its scenarios registered.

**Exit.** Pass when:
- every sentence of a rendered page is traced to a stored brick, shown by planting a sentence that
  is not and seeing the render refuse;
- every number on the page is signed by the verifier;
- the comparison of two consecutive reports attributes every difference to at least one cause;
- a revision replay of a past report runs with its cards held fixed;
- the export's reader, given planted records of every kind, returns none that became available
  after its instant;
- the comparison of two reports reuses stored model responses wherever its inputs are unchanged.

## Steps

1. **Verifier and renderer.** *Execution.* Anchors re-read and signed; bricks and rows to page, with
   refusal of any value not signed.
2. **Formats.** *Design.* The short note and the study; a sober, readable layout.
3. **Manifest.** *Execution.* Every report as a list of row identifiers and card versions.
4. **Comparison.** *Design and execution.* The attribution of differences to causes.
5. **Revision replay.** *Execution.* The same report, cards fixed, on a later vintage.
6. **Export.** *Design and execution.* Facts, atoms, states and cards, partitioned by availability,
   with the `as_of` reader.

## Deliverables

- The renderer and its two formats.
- Report manifests.
- The comparison and the revision replay.
- The point-in-time export and its documentation.

## What it refuses

| It refuses | Because |
|---|---|
| A sentence that is not a stored brick | The page would say something the store does not. |
| A number that does not re-read to its anchor | It cannot be traced. |
| A comparison difference with no cause | Every change has a reason, and the reason is the information. |
| A replay or counterfactual row in the analysis tables | Only live analysis is analysis. |
| A record read before it became available | That would be hindsight. |
| A recommendation | Atlas analyses; it does not advise. |
