[← L4](L4-analysis.md) · [Up: Blueprint](README.md) · [L6 →](L6-outputs.md)

# L5 — Scenarios and score

## TL;DR

Atlas writes conditional scenarios, not forecasts: at least two branches, each with an observable trigger, an invalidation and an outcome defined before the date.
Every scenario is registered, append-only, and judged when its horizon passes, against the data vintage it targeted.
A failure goes back to the card that produced it; over years, the verdicts become a map of which lens works for which kind of situation.

## Purpose

Make every forward-looking statement **scoreable**, and score it honestly: on the data available at
the time, at the date fixed in advance, by the definition fixed in advance.

**Success looks like:**
- No scenario reaches the registry without passing the validity rules.
- Every registered scenario receives a verdict at its judgement date, without anyone choosing when.
- Every verdict can be traced back to the card version and lens behind it.

## What makes a scenario set valid

These are rules checked by code, not guidelines. A scenario set is refused if:

- **it has fewer than two branches.** One branch is a forecast wearing the word "scenario";
- **a branch lacks an observable trigger, an invalidation condition or an outcome definition.** A
  branch that cannot be wrong can never be scored;
- **its outcome definition was registered after its date.** What counts as the outcome is fixed when
  the scenario is written, so the goalposts cannot move.

Each branch also states its horizon and the lens whose mechanism it follows. **Branch strengths are
not probabilities and are never normalised to 100 %**: each says how strongly its branch is
supported, so a total well below 100 % openly shows how much is unknown. "Not enough information"
is a valid output.

## Judging

A scenario set cannot be judged before its horizon passes; judging early would mean choosing the
moment one happens to be right. The judgement date is derived from the horizon at registration.
Each branch is then declared:

| Verdict | When |
|---|---|
| **Realised** | its trigger was observed and its outcome definition met |
| **Invalidated** | its invalidation condition was observed |
| **Not realised** | it was watched, and it did not happen |
| **Undecidable** | it could not be observed: a series discontinued, a release missing |
| **Contradictory specification** | both its trigger and its invalidation occurred, a defect of the card, not a verdict |

**Judged against the targeted vintage.** A scenario about inflation over the next twelve months is
judged on the data as first published at the horizon, if that is what it targeted, not on figures
revised two years later. The outcome definition says which vintage counts.

## Historical analogues, with a null test

"This looks like 1973" is one of the most common arguments in macro, and one of the least tested.
Atlas puts forward a historical analogue only if:

- **its match beats chance in the same history.** Thirty random other moments of the same history
  are drawn, each one's closest match elsewhere is found, and the analogue is kept only if the real
  match is closer than all of them;
- **the method, tested as a whole, does not find equally good matches in unrelated histories.** If
  it does, it is matching noise;
- **it is published with its distance, the number of past states searched and the number of exact
  ties.**

No distance threshold is tuned; the number of draws is fixed and logged, and it sets how strict the
test is.

## Keeping score

- **Live only.** A model knows how history turned out, so only scenarios produced on their own date
  count. There is no backtest of reasoning ([principle 8](principles.md#8-analysis-is-clean-from-its-production-date)).
- **Tagged at birth.** Every scenario carries its economy, subject, horizon, lens and card version.
  Without the tag, a verdict cannot be credited to a way of reasoning.
- **Multiple testing on the record.** A system that scores thousands of branches will find lenses
  that look good by chance. The evaluation records how many were tested, and a claim that a lens
  works must survive that count.
- **Slow by nature.** The United States has had about a dozen recessions since the Second World
  War; rare events give few test cases. The record starts with the first live report and only
  accumulates forward.

## The loop

A branch judged wrong, or a set judged undecidable because its trigger could not be observed, puts
its card in the workshop queue ([L3](L3-subject-cards.md)) with the verdict attached. The card is
revised, audited and versioned; the verdict stays in the registry against the old version.

## Interfaces

| Direction | Artefact | From / to |
|---|---|---|
| in | Instantiated scenario sets | [L4](L4-analysis.md) |
| in | As-of reads at the judgement date, on the targeted vintage | [L1](L1-facts.md) |
| out | Scenario registry: sets, judgement dates, verdicts | [L6](L6-outputs.md) |
| out | Failed and undecidable scenarios | [L3](L3-subject-cards.md) workshop queue |
| out | Verdicts by lens, subject and horizon | [L6](L6-outputs.md) export |

## Gates

**Entry.** The analysis store holds scenario sets with their outcome definitions.

**Exit.** Pass when:
- each validity rule is shown to refuse a planted invalid set;
- a set registered with a past outcome definition is refused;
- verdicts are computed on the targeted vintage, shown on a series whose revision changes the
  verdict;
- a judged failure reaches the workshop queue with its card version.

## Steps

1. **Validity rules.** *Execution.* The three refusals, in code.
2. **Registry.** *Execution.* Append-only, with the judgement date derived at registration.
3. **Judgement.** *Design and execution.* The five outcomes, the vintage rule, the undecidable case.
4. **Analogues.** *Design and execution.* The null test, fixed and logged.
5. **Loop.** *Execution.* Verdicts back to the workshop queue.
6. **Evaluation by lens.** *Design.* The tag at birth and the multiple-testing record.

## Deliverables

- The scenario validator.
- The append-only registry and its judge.
- The analogue rule with its null test.
- The table of verdicts by economy, subject, horizon and lens.

## What it refuses

| It refuses | Because |
|---|---|
| A single-branch scenario | It is a forecast. |
| A branch with no trigger, invalidation or outcome | It cannot be scored. |
| An outcome defined after the date | The goalposts would move. |
| A verdict before the horizon | It would let the judge choose the moment. |
| A verdict on revised data when the scenario targeted first releases | It would judge the call on data nobody had. |
| Scoring an analysis produced after the fact | The model knows how history turned out. |
