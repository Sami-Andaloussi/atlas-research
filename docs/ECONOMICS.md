# The economic method

What the economics layer of Atlas is for, what exists today, and what does not.

The question it is built to answer, for any situation:

> **Which explanations compete here, what does each one expect, and how will we know which was
> right?**

**Status, 2026-09-24.** The theory map and the rules for a valid scenario are written. The engine
does not yet apply lenses to data, so no scenario has been produced from real data and there is no
track record. Each section below says which of its parts exist and which are design. Counts were
taken in the private repository on 2026-09-24.

---

## 1. A map of theories, not a house view

Most research has a house view. Atlas has a map: **23 families of economic theory, holding 72 named
lenses.** Most lenses are competing explanations. Some are meant to be used together rather than
chosen between: the four accounting lenses (income, financing, external and sectoral balances) are
identities that must all hold at once, and the crisis lenses are mechanisms that often fire together.

| Group | Family | Lenses |
|---|---|:--:|
| **Macro and policy** | Business cycle | 3 |
| | Inflation and price setting | 3 |
| | Monetary policy and credit | 2 |
| | Fiscal policy and public finance | 3 |
| | Open economy and exchange rates | 2 |
| | Macroeconomic accounting | 4 |
| **Markets and finance** | Asset pricing | 3 |
| | Financial and sovereign crises | 6 |
| | Corporate finance and governance | 3 |
| | Behaviour and narratives | 3 |
| **Real economy and structure** | Growth and development | 2 |
| | Structural transformation | 2 |
| | International trade | 2 |
| | Industrial organisation | 2 |
| | Technology and innovation | 2 |
| | Commodities and resources | 6 |
| | Labour and demographics | 6 |
| | Spatial economics and networks | 2 |
| | Environment and climate | 3 |
| **Institutions and society** | Institutions and political economy | 2 |
| | Geopolitics and security | 3 |
| | Informal economy | 6 |
| | Individual choice and games | 2 |
| | **Total** | **72** |

**The counts are uneven, and the table shows it on purpose.** Several families a macro reader looks at
first (monetary policy, exchange rates, growth) hold two lenses today, so the map offers only two
readings from inside each of those families. A question is not limited to one family, though: a
monetary question can also draw on the business-cycle, inflation and fiscal lenses.

Beside the theory map, the catalogue holds **26 method families** (52 method routes), **18 families of
formal models** (general equilibrium, stock-flow consistent, input-output, term structure, state space
and others), **22 algorithm families**, and **64 reference works**.

---

## 2. What a lens has to declare

A lens is not a label. Each of the 72 declares:

- the **assumptions** it relies on, and the **inputs** it needs;
- the **outputs** it is allowed to produce, and its known **limitations**;
- its **alternatives**: competing lenses, theory families or model types;
- a **counterexample**: a situation where it fails;
- a **baseline**: the simpler reading it has to beat to be worth using;
- **disconfirming outcomes**: what would count against it;
- **robustness checks**, and a **retirement rule**: when to stop using it;
- its **references**, or a declared gap where the catalogue does not yet hold a suitable work. That is
  the case for 20 of the 72 today, concentrated in the families that hold six lenses.

An illustration taken from the map: inflation, three lenses. This is catalogue content, not an
analysis. It shows how the question is framed, not what the answer is today.

| Lens | Explains inflation through… | What would count against it, as the map states it |
|---|---|---|
| **New Keynesian (sticky prices)** | staggered price adjustment and forward-looking expectations | "expectations stay anchored yet [the lens] misses [a] realized inflation burst" |
| **Conflict and cost-push** | cost shocks, defence of margins, and wage–price bargaining | "cost and margin measures rise yet broad inflation does not propagate" |
| **Fiscal theory of the price level** | the price level adjusting so that the real value of government debt equals the present value of expected primary surpluses, when fiscal policy rather than the central bank pins it down | "debt and deficits jump yet the price level tracks the monetary rule, not the fiscal constraint" |

Three serious explanations, each with the outcome that would count against it. A reader who only ever
hears one of them is missing most of the argument.

---

## 3. Keeping explanations apart

*Design rules. Lenses are not yet applied to data.*

- **Same snapshot.** Every lens will read from the same frozen snapshot of the store, as of the same
  date. Each lens takes the inputs it declares; none gets a fresher or a revised version of the data.
- **No cross-talk.** No lens will see another lens's conclusions, so a monetary reading cannot be
  nudged by a fiscal one.
- **Disagreement is data.** When lenses disagree, the disagreement will be kept rather than averaged
  away. If five explanations are plausible, all five stay.
- **Declared bias, not absent bias.** Choosing which theories belong on the map is itself a choice.
  That is why the per-family counts are published here, and why every output will name the lenses it
  used, so a reader can see what each would have said.

---

## 4. Claims are typed

A statement in Atlas is not free text. The contract distinguishes **11 kinds of claim**: description,
measurement, association, identity, causal effect, causal mechanism, forecast, scenario condition,
valuation, legal status, and normative.

This matters because the classic errors in economic commentary are type errors: a correlation
presented as a cause, an accounting identity presented as behaviour, a forecast presented as a fact.
Typing cannot stop someone from mislabelling a claim, but it makes the causal label expensive. Two
rules in the contract apply: any causal claim must name its mechanism, the competing explanations, and
the condition that would refute it; and a claim typed as a causal effect or a causal mechanism must
also name the inference method behind it.

Missing data gets the same care. A value is either present or absent in one of **eleven distinct
ways**: missing, not observed, not applicable, suppressed, censored, below detection limit, withheld,
invalid, not yet released, inaccessible, or in unresolved conflict. An absence is never turned into a
zero, a "false" or an empty value.

---

## 5. What makes a scenario valid

*Coded and tested on test cases. No scenario has yet been generated from real data.*

These are rules checked by code, not guidelines. A scenario set is refused if:

- **it has fewer than two branches.** One branch is a forecast wearing the word "scenario";
- **a branch lacks an observable trigger, an invalidation condition, or an outcome definition.** A
  branch that cannot be wrong can never be scored;
- **an outcome definition was registered after the scenario's as-of date.** What counts as the outcome
  is fixed when the scenario is written, so the goalposts cannot move.

**Branch strengths are never normalised to 100%.** They are not probabilities: each says how strongly
its branch is supported, so a total well below 100% openly shows how much is unknown, instead of
spreading that ignorance across branches. "Not enough information" is a valid output.

A set cannot be scored before its horizon has passed; scoring early would mean choosing the moment
when you happen to be right. Each branch is then marked **realised** (its trigger was observed),
**invalidated** (its invalidation condition was observed), **not realised** (watched, and it did not
happen) or **undecidable** (it could not be observed). A branch whose trigger and invalidation both
occurred is flagged as a **contradictory specification** instead of being quietly given a verdict.

In the current rule, a verdict is read from the trigger and the invalidation condition. Checking the
pre-registered outcome itself belongs to the scoring work described in section 7, which has not
started.

---

## 6. Historical analogues, with a null test

*Implemented and tested on a synthetic history. Not yet run on real data.*

"This looks like 1973" is one of the most common arguments in macroeconomics, and one of the least
tested. Atlas will only put forward a historical analogue if:

- **its match is closer than those found for other moments of the same history.** Any series can find
  some past that looks like it. Atlas makes 30 random draws of other moments from the same history,
  finds each one's closest match elsewhere in that history, and emits the analogue only if the real
  match beats all of them;
- **the method, tested as a whole, does not find equally good matches in other subjects' histories.**
  Today this is checked on the synthetic test set, not for each analogue. If it finds them, it is
  matching noise; for related economies, where a cross-country parallel may be genuine, the rule will
  need refining before it runs on real data;
- **it comes with its distance, the number of past states searched, and the number of exact ties.**

No distance threshold is tuned. The number of draws is fixed and logged, and it sets how strict the
test is.

---

## 7. Keeping score

*Not started. The scoring arc (arc 08, "Bench and algorithm map" in the [roadmap](ROADMAP.md)) has 0
of its 11 steps done.*

- **Judged against the right vintage.** A forecast or scenario will be scored against the data vintage
  it was aimed at, not against numbers revised years later.
- **Tagged at birth.** Every output will carry a tag (day, subject, scale, lens, method). Without it,
  a result cannot be credited to a way of reasoning.
- **Multiple testing on the record.** The evaluation contract has a required field for how multiple
  testing is handled, and a confirmatory experiment must pre-register its testing plan. A system that
  scores thousands of outputs will find lenses that look good by chance.
- **Slow by nature.** The result, built over years, is a map of which lens works for which kind of
  situation.

---

## 8. What this is not

- **Not a forecasting shop.** Atlas is being built to write conditional scenarios first. Where it will
  make a numeric forecast, the forecast is typed as one and will be scored as one.
- **Not a house view.** Several explanations stand side by side.
- **Language models are a tool, not the analyst.** Code extracts candidate values; a language model
  chooses one or abstains. Models are not a source of facts or of theory.
- **Not investment advice.**

---

## Where these statements come from

Everything above describes the private repository and cannot be verified from this one.

| Statement | Private repository path |
|---|---|
| 23 families, 72 lenses, the fields each lens declares, reference gaps, the inflation example | `methods/catalogs/theory/` |
| Method, model and algorithm families, reference works | `methods/catalogs/` |
| The 11 claim kinds | `core/contract/sections/enums.yaml` |
| Causal-claim rules, pre-registered testing plan | `core/contract/rules/conditional_rules__part_001.yaml` |
| The 11 kinds of absence (12 statuses with "present") | `data/families.yaml` |
| Multiple-testing field | `core/contract/objects/Evaluation.yaml` |
| Scenario rules and branch verdicts | `validation/scenario_set.py`, `validation/scenario_declencheurs.py` |
| Historical-analogue rule | `validation/analogue/`, plan item `A07-8` |
| Scoring arc, 0 of 11 | plan arc `08` |
