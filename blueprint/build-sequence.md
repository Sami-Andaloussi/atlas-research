[Up: Blueprint](README.md)

# Build sequence

## TL;DR

Atlas is built along one subject first: US inflation, from the source to its first registered scenario, before any breadth.
Then depth on the United States, then Switzerland and the euro area by adding sources, lenses and cards, never by changing the engine, then the loop that turns real gaps into cards.
Each phase ends on a test it must pass, checked by a reviewer who did not build it.

## The phases

```mermaid
flowchart LR
    p0["0 · The frame"] --> p1["1 · US facts"]
    p0 --> p2["2 · Theory map and first card"]
    p1 -.->|history to calibrate on| p2
    p1 --> p3["3 · Analysis and registry"]
    p2 --> p3
    p3 --> p4["4 · Report and export"]
    p3 --> p5["5 · Score"]
    p4 --> m1(["Milestone · US inflation end to end"])
    p5 --> p8
    m1 --> p6["6 · US depth"]
    m1 --> p7["7 · Switzerland and euro area"]
    p6 --> p8["8 · The loop"]
    p7 --> p8
```

| Phase | What it builds | Layers | Done when |
|---|---|---|---|
| **0 · The frame** | The rules of the build, the [data contracts](data-contracts.md), access to the sources, the model behind the menus | All | Every source of the first economy has answered a real download; for Switzerland and the euro area, the same base series have been downloaded from their official sources, or the economy waits; one call to the model has returned a structured choice, with its latency and cost measured. |
| **1 · US facts** | The series catalogue, capture, anchoring, vintages, the as-of read, capture from the release calendar | [L1](L1-facts.md) | Every value re-reads from its bytes; the as-of read cannot see a planted later vintage; capture runs from the calendar. |
| **2 · Theory map and first card** | The lens catalogue, the inflation and rates families deepened, the card format, the workshop, the US inflation card | [L2](L2-theory-map.md), [L3](L3-subject-cards.md) | The inflation card passes its schema and its isolated audit, calibrated on the history phase 1 captured; every lens it cites is complete. |
| **3 · Analysis and registry** | The frozen packet, rules, menu choices, checks, the residual, the analysis store, coverage; scenario validation, the registry and a historical judge; the inflation card's out-of-sample test | [L3](L3-subject-cards.md), [L4](L4-analysis.md), [L5](L5-scenarios-score.md) | The packet agrees with an independent calculation on real dates; a planted bad pick becomes an abstention; a run replays deterministically; an invalid scenario set is refused; the inflation card passes its out-of-sample test and is accepted. |
| **4 · Report and export** | The renderer, the two formats, report manifests, the point-in-time export | [L6](L6-outputs.md) | A planted sentence that is not a brick makes the render refuse; the export hides every analysis row before its production date. |
| **5 · Score** | Live judgement on the targeted vintage, scoring against baselines and benchmarks, the loop to the workshop | [L5](L5-scenarios-score.md) | A revision that should change a state does; a void branch is not scored; a missed outcome reaches the workshop. |
| **Milestone** | US inflation, end to end | All | Facts, card, analysis, report, export and one registered scenario, for one live date; the first report has been read by a human before anything is published. |
| **6 · US depth** | Cards for growth, jobs, the Fed and rates, credit, the budget, the external accounts and the dollar, housing; every lens's inputs wired to series; regular reports; cards that compose others | [L1](L1-facts.md)–[L6](L6-outputs.md) | Every US subject has an accepted card; a report runs at each major release; a composed card passes its out-of-sample test. |
| **7 · Switzerland and euro area** | Their series and sources; the lenses they need that the map lacks (the franc as a safe haven, exchange-rate intervention); cards adapted to them: the SNB and the franc, the ECB and the euro area | [L1](L1-facts.md), [L2](L2-theory-map.md), [L3](L3-subject-cards.md) | Reports run for both, and the engine was not modified to get there. If it was, the change is recorded and its cause removed. |
| **8 · The loop** | Real abstentions turned into cards, a dashboard of coverage, model cost, reports and scenarios awaiting judgement | [L3](L3-subject-cards.md)–[L5](L5-scenarios-score.md) | At least one "not covered" from production has become an audited card that a later report used; a final isolated review against the [principles](principles.md) finds nothing blocking. |

## Why this order

- **One subject end to end before breadth.** A chain that works on one subject proves every
  interface between layers; seven half-built subjects prove none. US inflation goes first because
  its data are long and public, because PCE prices and the seasonal factors behind every monthly
  pace are revised, and because it is where competing lenses disagree most visibly.
- **Facts and knowledge side by side.** The lens catalogue and the card format do not need the
  store; only the card's calibration does. So phase 2 starts with phase 1 and accepts its card once
  phase 1 has captured the history.
- **Registry with the analysis, score before depth.** A scenario is registered by the run that
  produces it, and a scenario that is never judged teaches nothing. The registry runs from the first
  live report, because the record only accumulates forward
  ([principle 8](principles.md#8-analysis-counts-from-the-day-it-was-made)).
- **Breadth by cards, as a test.** Phase 7 is the proof of [principle 5](principles.md#5-knowledge-in-cards-not-in-code):
  if adding an economy needs a change to the engine, the design has failed somewhere, and the
  phase says where.
- **The loop last, on real gaps.** The workshop queue is only worth tuning once production has
  filled it with real abstentions.

## How a phase closes

1. Every step of the phase is done, each in its own change, with its proof.
2. The phase's exit checks pass, or each failure is explained in writing.
3. **An isolated review**: a reviewer who built nothing in the phase checks it against the
   principles. Findings are fixed or answered in writing.
4. The phase closes when the review finds nothing blocking.

## After the sequence

Other economies, then sectors, companies and assets, enter the same way: sources added to the
catalogue, lenses and cards written and audited in the workshop. The engine does not change.
