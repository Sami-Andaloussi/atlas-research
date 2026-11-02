[Up: Blueprint](README.md)

# Design principles

## TL;DR

Ten rules every layer follows.
Each gives the rule, why it matters, and where it shows.
They come in pairs of concerns: what counts as a fact, what counts as analysis, who decides, and how the system learns.

| # | Principle | The rule in one sentence |
|---|---|---|
| 1 | [Exact or absent](#1-exact-or-absent) | A value traces back to its bytes, or it is refused; an absence is typed, never a zero. |
| 2 | [What was known, when](#2-what-was-known-when) | Every read names a date and cannot see past it; a revision adds a vintage and erases nothing. |
| 3 | [No free text](#3-no-free-text) | What can be scored is a structured choice; what explains is pre-written text attached to it. |
| 4 | [Rule, then menu, then abstain](#4-rule-then-menu-then-abstain) | Code decides first; a language model only picks from a filtered menu; otherwise the engine says "not covered". |
| 5 | [Knowledge in cards, not in code](#5-knowledge-in-cards-not-in-code) | Thresholds, texts, scenarios and menus live in versioned cards; the engine stays generic. |
| 6 | [No house view](#6-no-house-view) | Competing explanations are kept side by side, and their disagreement is data. |
| 7 | [Falsifiable before it exists](#7-falsifiable-before-it-exists) | A scenario has an observable trigger, an invalidation and an outcome fixed before its date, or it is refused. |
| 8 | [Analysis is clean from its production date](#8-analysis-is-clean-from-its-production-date) | Facts can be replayed over all history; analysis is tested only from the day it was produced. |
| 9 | [The producer is never the judge](#9-the-producer-is-never-the-judge) | No card, rule or output is accepted on the word of whoever produced it. |
| 10 | [Coverage is measured](#10-coverage-is-measured) | Every run says how much came from rules, from menu choices, and what was left uncovered. |

## 1. Exact or absent

**Rule.** A value in Atlas is the value printed in a captured document, at a known byte range, or
it is not in Atlas. When a value is missing it is recorded as one of eleven kinds of absence:
missing, not observed, not applicable, suppressed, censored, below detection limit, withheld,
invalid, not yet released, inaccessible, or in unresolved conflict.

**Why.** A report that cannot show where its number came from cannot be checked, and a zero that
stands for "we do not know" becomes a fact in every calculation downstream.

**Where it shows.** Capture keeps bytes, not strings, and anchoring binds a value to a slice of
them ([L1](L1-facts.md)). A computed quantity that cannot be computed is `None` with its reason
([L4](L4-analysis.md)).

## 2. What was known, when

**Rule.** Every value carries four dates: when the source published it, when Atlas captured it,
when it became known, and when it entered the store. Every read is a read *as of* a date, and the
reading function is unable to return anything known after that date.

**Why.** GDP, payrolls and inflation are revised for years. Judging a past reading against today's
numbers is unfair in both directions: it punishes a call that was right on the data of its day,
and rewards one fitted to data nobody had.

**Where it shows.** The point-in-time store ([L1](L1-facts.md)), the frozen packet of every
analysis ([L4](L4-analysis.md)), scoring against the targeted vintage ([L5](L5-scenarios-score.md))
and the revision replay of a report ([L6](L6-outputs.md)).

## 3. No free text

**Rule.** Everything that will be scored or queried is a structured choice: a named series, a
threshold, a date, the identifier of a card entry. Everything that explains is pre-written text,
written in the workshop, attached to those choices, with holes for the numbers.

**Why.** Prose cannot be compared, queried or scored. A structured choice can be compared with the
next report's, counted across a thousand reports, and judged when its horizon passes.

**Where it shows.** Text bricks in the cards ([L3](L3-subject-cards.md)), analysis rows
([L4](L4-analysis.md)), reports assembled word for word from stored rows ([L6](L6-outputs.md)).

## 4. Rule, then menu, then abstain

**Rule.** Each decision of the engine is taken in this order, without exception:

1. **a code rule**, wherever one is possible: thresholds, trends, decompositions, calendars;
2. **otherwise a choice**: code filters a short menu of pre-written options to those whose
   conditions hold, and a language model picks one, with a verbatim quotation where the card
   requires one, or abstains;
3. **otherwise an abstention**: "not covered", which goes to the workshop queue.

Code then checks every choice. A quotation must exist word for word in its source; a choice that
says "driven by energy" must be confirmed by the computed contribution. A choice that fails a
check becomes an abstention, never a published error.

**Why.** A language model is good at reading a situation and weak as a source of facts. Used as a
selector over vetted options, its strength is kept and its failure modes are fenced off: it can
pick the wrong option, which code catches, but it cannot invent a number or a sentence.

**Where it shows.** [L4](L4-analysis.md) runs the order; [L3](L3-subject-cards.md) writes the
menus; every choice keeps its run log (model, prompt version, card versions, date, data seen).

## 5. Knowledge in cards, not in code

**Rule.** Thresholds, text bricks, scenario templates and menus live in subject cards, versioned
and fingerprinted. The engine only knows a closed set of operations (year-on-year, annualised
pace, average, gap, linear combination) and how to evaluate a card.

**Why.** Extending Atlas to a new subject, a new theory or a new economy should be writing and
auditing a card, not a change to the engine that could break every subject at once.

**Where it shows.** [L3](L3-subject-cards.md); the build sequence proves it by adding Switzerland
and the euro area through sources and cards alone ([build sequence](build-sequence.md)).

## 6. No house view

**Rule.** Where several lenses of the theory map read a situation, all of them are kept, with what
each reads and what each would expect. Disagreement between them is stored, not averaged away.
Choosing which theories are on the map is itself a choice, so the map is published with its
per-family counts.

**Why.** The most useful information in a macro debate is where serious explanations disagree and
why. A reader who only hears one lens is missing most of the argument.

**Where it shows.** [L2](L2-theory-map.md); every output names the lenses it used.

## 7. Falsifiable before it exists

**Rule.** A scenario set is refused if it has fewer than two branches, if a branch lacks an
observable trigger, an invalidation condition or an outcome definition, or if its outcome
definition was registered after the set's date. Branch strengths are never normalised to 100 %.

**Why.** A branch that cannot be wrong cannot be scored, and an outcome defined after the fact lets
the goalposts move.

**Where it shows.** [L5](L5-scenarios-score.md).

## 8. Analysis is clean from its production date

**Rule.** Facts are clean over all history, thanks to vintages. Analysis is not: a language model
knows how history turned out. So no analysis is ever tested before the date it was produced, and
the export says so.

**Why.** A backtest of reasoning run today over 2008 would be graded by a model that has read about
2008. That is hindsight, not evidence.

**Where it shows.** The point-in-time export ([L6](L6-outputs.md)); the score counts only scenarios
produced live ([L5](L5-scenarios-score.md)). It is also why production starts early: the record
only accumulates forward.

## 9. The producer is never the judge

**Rule.** A card is written by one party and audited by another that wrote none of it, against its
sources and on data it was not calibrated on. A change to the engine is accepted on a check that
can fail, shown to fail on a deliberate break, never on the word of whoever made it.

**Why.** A producer is a weak judge of its own work: confident fixes that test nothing look the same
as real ones until someone else looks.

**Where it shows.** The workshop audit and out-of-sample test of every card
([L3](L3-subject-cards.md)); the review that closes every phase ([build sequence](build-sequence.md)).

## 10. Coverage is measured

**Rule.** Every run publishes, for its subject and date, the share of decisions taken by code rules,
by menu choices, and the share that ended in "not covered".

**Why.** That ratio is the direct measure of what Atlas exists to do: move discretionary analysis
into data. It also shows where the cards are thin.

**Where it shows.** [L4](L4-analysis.md) computes it, [L6](L6-outputs.md) prints it, and the last
phase of the [build sequence](build-sequence.md) turns real abstentions into cards.
