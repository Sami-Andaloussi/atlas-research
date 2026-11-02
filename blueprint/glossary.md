[Up: Blueprint](README.md)

# Glossary

| Term | Meaning |
|---|---|
| <a id="abstention"></a>**Abstention** | The engine's answer when neither a rule nor a menu choice can decide: "not covered". A valid output, sent to the workshop queue. |
| <a id="absence"></a>**Absence** | A value that is not there, recorded as one of eleven kinds: missing, not observed, not applicable, suppressed, censored, below detection limit, withheld, invalid, not yet released, inaccessible, in unresolved conflict. Never a zero. |
| <a id="analysis-row"></a>**Analysis row** | One dated decision of the engine (a situation held, a lens reading, a menu pick, a scenario, an abstention), with its run log. |
| <a id="anchor"></a>**Anchor** | The byte range of a captured document a value was read from. Re-reading it must give back the value. |
| <a id="as-of"></a>**As of** | The date a read is made from. A read as of a date returns only what was known on that date. |
| <a id="baseline"></a>**Baseline** | The simpler reading a lens must beat to be worth using. |
| <a id="brick"></a>**Text brick** | A pre-written sentence attached to a situation or a lens reading, with holes for numbers and two or three equivalent variants. |
| <a id="capture"></a>**Capture** | Retrieving a source's bytes, unmodified, with a fingerprint and a capture date. |
| <a id="card"></a>**Subject card** | The versioned file that holds the knowledge for one economy and subject: series, quantities, situations, lenses, bricks, scenario templates, menus. |
| <a id="claim"></a>**Claim** | A typed statement. Eleven kinds: description, measurement, association, identity, causal effect, causal mechanism, forecast, scenario condition, valuation, legal status, normative. |
| <a id="counterexample"></a>**Counterexample** | A situation, dated where possible, in which a lens fails. |
| <a id="coverage"></a>**Coverage** | For a run: the share of decisions taken by rules, by menu choices, and left uncovered. |
| <a id="family"></a>**Family** | A group of lenses on the same domain, such as monetary policy and credit. The map holds 23. |
| <a id="fingerprint"></a>**Fingerprint** | A hash that identifies a document or a card version exactly. |
| <a id="frozen-packet"></a>**Frozen packet** | Everything an analysis may see for a subject and a date: the as-of facts and the quantities computed from them, with their anchors. |
| <a id="judgement-date"></a>**Judgement date** | The date a scenario is judged, derived from its horizon when it is registered. |
| <a id="lens"></a>**Lens** | A named economic explanation on the theory map, with its assumptions, inputs, counterexample, baseline and disconfirming outcomes. The map holds 72. |
| <a id="menu"></a>**Menu** | A short list of pre-written options for a judgement the card leaves open. Code filters it; a language model picks one or abstains. |
| <a id="outcome-definition"></a>**Outcome definition** | What counts as a branch coming true, fixed before the scenario's date. |
| <a id="point-in-time"></a>**Point in time** | Kept so that any past date can be replayed with exactly what was known then. |
| <a id="quantity"></a>**Quantity** | A value computed by a card from series, with a closed set of operations: year-on-year, annualised pace, average, gap, absolute value, linear combination. |
| <a id="registry"></a>**Scenario registry** | The append-only record of every scenario set, its judgement date and its verdicts. |
| <a id="revision-replay"></a>**Revision replay** | A past report rerun with its cards held fixed on a later vintage of the data, to see what the revisions alone change. |
| <a id="run-log"></a>**Run log** | What a run could see and used: model and version, prompt version, card versions, date, data identifiers. |
| <a id="scenario"></a>**Scenario set** | At least two branches, each with an observable trigger, an invalidation, a horizon and an outcome definition. |
| <a id="situation"></a>**Situation** | A code condition on quantities, declared in a card, such as "core PCE more than half a point above 2 %". |
| <a id="verdict"></a>**Verdict** | The judgement of a branch at its horizon: realised, invalidated, not realised, undecidable, or a contradictory specification. |
| <a id="vintage"></a>**Vintage** | The version of a series published on a given date. A revision adds a vintage and erases none. |
| <a id="workshop"></a>**Workshop** | Where cards are written from sources, audited by someone else, tested out of sample and versioned; fed by new subjects, abstentions and failed scenarios. |
