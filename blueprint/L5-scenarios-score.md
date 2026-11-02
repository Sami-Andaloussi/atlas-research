[← L4](L4-analysis.md) · [Up: Blueprint](README.md) · [L6 →](L6-outputs.md)

# L5 — Scenarios and score

## TL;DR

Atlas writes conditional scenarios, not forecasts: if a trigger fires, an outcome follows by the horizon, unless an invalidation comes first.
Every scenario is registered, append-only, and judged when the release it targeted comes out, on that vintage.
A branch is credited to its lens only if it beats the lens's baseline, with the evidence of the lens's own mechanism; failures go back to the card that produced them.

## Purpose

Make every forward-looking statement **scoreable**, and score it honestly: on the data available at
the time, at a date fixed in advance, by a definition fixed in advance, against a benchmark.

**Success looks like:**
- No scenario reaches the registry without passing the validity rules.
- Every registered scenario receives a state at its judgement date, without anyone choosing when.
- Every verdict can be traced to the card version and lens behind it.

## What makes a scenario set valid

These are rules checked by code, not guidelines. A scenario set is refused if:

- **it has fewer than two branches.** One branch is a forecast wearing the word "scenario";
- **a branch lacks an observable trigger, an invalidation condition, an outcome definition, a
  horizon, a lens, or the vintage it targets.** A branch that cannot be wrong, or cannot be
  credited, cannot be scored;
- **it was registered after the run that produced it**, or its observation window opens before its
  registration. What counts as the outcome is fixed when the scenario is written, so the goalposts
  cannot move.

Each branch carries a **strength** set by the card: weak, moderate or strong. It is an ordinal
ranking, not a probability. A branch receives a probability only once the card's strengths have been
calibrated on the live record, and from then on it is scored with a proper scoring rule (the Brier
score). "Not enough information" is a valid output.

## Judging

The judgement date is fixed at registration: the release date, from the publisher's calendar, of the
vintage the branch targets for its horizon period. A CPI branch with a twelve-month horizon is judged
when that month's CPI comes out, about two weeks after the month ends. If the release has not come
out within a stated delay, the branch is undecidable.

Each branch then takes one state:

| State | When |
|---|---|
| **Void** | its trigger never fired before the horizon: the condition was not met, and nothing is scored |
| **Invalidated** | its invalidation was observed first, before the outcome |
| **Outcome met** | its trigger fired and its outcome definition is met on the targeted vintage |
| **Outcome missed** | its trigger fired and its outcome definition is not met |
| **Undecidable** | it could not be observed: a series discontinued, a release missing |

Where a trigger and an invalidation are both observed, the first observed wins. A branch whose trigger
and invalidation can be met by the same observation is a defect of the card, flagged as a
**contradictory specification** and sent to the workshop, not judged.

**Judged against the targeted vintage.** A branch about inflation over the next twelve months is
judged on the data as first released at the horizon if that is what it targeted, not on figures
revised two years later. The branch's targeted vintage is part of its definition.

## Historical analogues, with a null test

"This looks like 1973" is one of the most common arguments in macro, and one of the least tested.
Where a card allows analogues, the card declares the state vector, its scaling, the distance and an
exclusion window; the analogue is then an L4 decision, and Atlas puts it forward only if:

- **its match beats chance in the same history.** Thirty other moments of the same history are
  drawn, each one's closest match outside its exclusion window is found, and the analogue is kept
  only if the real match is closer than all of them. The rank is logged;
- **the method, tested as a whole, does not find equally good matches in comparison histories**:
  other economies, and the same series shuffled in blocks. If it does, it is matching noise;
- **it is published with its distance, the number of past states searched and the number of exact
  ties.**

The state vector, the distance and the number of draws are fixed in the card before use and logged
with every analogue.

## Keeping score

- **Live only.** Only scenarios produced on their own date count. There is no backtest of reasoning
  ([principle 8](principles.md#8-analysis-is-clean-from-its-production-date)).
- **Against a benchmark.** Each lens is scored on its fired branches against its own baseline and
  against named benchmarks: no change, published consensus (the Survey of Professional
  Forecasters), the central bank's own projections. A set whose branches together cover every
  outcome earns no credit by that alone, because each branch is compared with what the benchmark
  expected.
- **Credited to a mechanism.** A branch names the observable that would show its lens's mechanism at
  work (wage growth for a cost-push branch, expectations for a sticky-price one). An outcome met
  without that evidence counts for the outcome, not for the lens.
- **Honest about overlap.** Monthly scenarios with twelve-month horizons overlap and are
  autocorrelated, so lenses are compared on non-overlapping windows or with errors corrected for
  overlap, and the number of lenses, subjects and horizons tested is recorded: a system that scores
  thousands of branches will find lenses that look good by chance.
- **Slow by nature.** The NBER dates about a dozen US recessions since 1945; rare events give few test
  cases. The record starts with the first live report, accumulates forward, and reports its void rate
  next to its hit rate.

## The loop

A branch whose outcome was missed, a branch left undecidable, and a contradictory specification each
put the card in the workshop queue ([L3](L3-subject-cards.md)) with the state attached. The card is
revised, audited and versioned; the state stays in the registry against the old version.

## Interfaces

| Direction | Artefact | From / to |
|---|---|---|
| in | Instantiated scenario sets | [L4](L4-analysis.md) |
| in | The read at the judgement date, on the targeted vintage; release calendars | [L1](L1-facts.md) |
| out | Scenario registry: sets, judgement dates, states | [L6](L6-outputs.md) |
| out | Missed, undecidable and contradictory branches | [L3](L3-subject-cards.md) workshop queue |
| out | Scores by lens, subject and horizon, with benchmarks | [L6](L6-outputs.md) export |

## Gates

**Entry.** The analysis store holds scenario sets with their outcome definitions and targeted
vintages.

**Exit.** Pass when:
- each validity rule is shown to refuse a planted invalid set;
- a set whose outcome definition was registered after its run is refused;
- states are computed on the targeted vintage, shown on a series whose revision changes the state;
- a void branch is not scored, and a missed outcome reaches the workshop queue with its card version;
- scores by lens are computed against the baseline and the named benchmarks.

## Steps

1. **Validity rules.** *Execution.* The refusals, in code.
2. **Registry.** *Execution.* Append-only and idempotent, with the judgement date fixed at
   registration from the release calendar.
3. **Judgement.** *Design and execution.* The five states, the precedence rule, the vintage rule.
4. **Analogues.** *Design and execution.* The declared specification and the null test.
5. **Scoring.** *Design.* Baselines, benchmarks, overlap, multiple testing, and the calibration of
   strengths into probabilities once the record allows it.
6. **Loop.** *Execution.* States back to the workshop queue.

## Deliverables

- The scenario validator.
- The append-only registry and its judge.
- The analogue rule with its null test.
- The table of scores by economy, subject, horizon and lens.

## What it refuses

| It refuses | Because |
|---|---|
| A single-branch scenario | It is a forecast. |
| A branch with no trigger, invalidation, outcome, horizon, lens or targeted vintage | It cannot be scored or credited. |
| An outcome defined after the run | The goalposts would move. |
| A verdict before the targeted release | It would let the judge choose the moment. |
| A verdict on revised data when the branch targeted first releases | It would judge the call on data nobody had. |
| Scoring a void branch as a miss | A condition that never came true is not a wrong call. |
| Scoring an analysis produced after the fact | Hindsight is not evidence. |
