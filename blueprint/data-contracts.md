[Up: Blueprint](README.md)

# Data contracts

## TL;DR

The identifiers, records and rules that let the six layers meet: what a fact, a run, an analysis row and a scenario are, field by field.
Time is stored as UTC timestamps, and every record carries the instant it became available, so any reader can be capped at any past instant.
Every store is append-only and idempotent: the same input twice adds nothing, and a wrong record is superseded, never edited.

## Time

| Field | Meaning |
|---|---|
| `period_start`, `period_end` | The period a value describes, half-open: `[start, end)`. |
| `published_at` | The publisher's official release instant (a CPI release at 08:30 New York time is stored as 12:30 or 13:30 UTC). |
| `known_at` | The instant from which a value counts as knowable. It equals `published_at` when the publisher or a real-time archive certifies the release, and `captured_at` otherwise. |
| `captured_at` | When Atlas retrieved the bytes. |
| `entered_at` | When the record entered the store. |
| `produced_at` | When a run actually executed. |
| `available_at` | On every record of every store: the instant it became available. `known_at` for a fact, `produced_at` for an analysis row, `registered_at` for a scenario, `judged_at` for a verdict. |

**The as-of rule.** A read as of an instant `t` returns only records with `available_at ≤ t`.
The boundary is inclusive: a CPI released at 12:30 UTC is visible to a read as of 12:30 UTC that
day, not to one as of 12:29.

## Identifiers

| Object | Identifier |
|---|---|
| Series | `economy.subject.measure.adjustment.transform`, e.g. `US.PRICES.PCE_CORE.SA.INDEX` |
| Series definition | `series_key@def_version`; a new definition version opens at a method break, a rebasing or a change of composition (the euro area gaining a member) |
| Document | SHA-256 of the response body |
| Vintage | `series_key/period/known_at`, with a `release_stage` (flash, advance, second, third, annual, benchmark) where the publisher names one |
| Card, lens | `card_id@version`, fingerprinted by SHA-256 of the canonicalised file, so reformatting does not change the fingerprint |
| Theory catalogue | `catalogue@version` |
| Run | SHA-256 of `(subject, as_of, card fingerprints, catalogue version, engine version, model, prompt version, mode)` |
| Row | `run_id/decision_kind/card_entry_id` |
| Scenario set, branch, verdict | `run_id/template_id`, `…/branch_id`, `…/branch_id/judged_at` |

## Records

**Fact.** `series_key, def_version, period_start, period_end, value | absence_type, unit,
release_stage, published_at, known_at, captured_at, entered_at, doc_fingerprint, anchors[],
source, point_in_time` (false for history that existed before Atlas's first capture of a source
with no real-time archive).

**Anchor.** `doc_fingerprint, decode_path, byte_start, byte_length, expected_text`. The decode
path reaches inside a container (`zip:xl/worksheets/sheet1.xml`, a PDF content stream); offsets
count in the decoded bytes. A check verifies the document's fingerprint first, then re-reads the
range.

**Run.** `run_id, subject, as_of, produced_at, mode (live | replay | counterfactual), engine_version,
card_fingerprints[], catalogue_version, model_id, prompt_version, sampling_parameters,
packet_fingerprint`.

**Analysis row.** `row_id, run_id, decision_kind (situation | lens_reading | menu_pick | scenario |
analogue | abstention), decided_by (rule | menu | auto | abstained), card_entry_id, claim_kind,
payload, available_at`. A menu pick also stores the option ids offered, the rendered prompt and
the raw response.

**Scenario branch.** `branch_id, set_id, lens_id, horizon, trigger, invalidation,
outcome_definition, target_vintage (first_release | release_stage | latest_at_judgement), strength
(ordinal: weak, moderate, strong, from the card), registered_at, judgement_date`.

**Verdict.** `branch_id, state, judged_at, vintage_read, evidence_rows[]`.

## The read

There is one read function, and every layer and the export go through it:

```
read(series_key, periods, as_of, vintage = as_of | first_release | stage(s) | nth(n))
```

Whatever the vintage selector, the result is capped by `as_of`: asking for the first release of a
period never returns a value known after `as_of`. Before Atlas's first capture of a source with no
real-time archive, the read returns the value flagged `point_in_time = false`; scoring and the
export's backtest reader refuse it.

## Idempotency and correction

- **Capture.** A document whose fingerprint is already archived is not stored again; the capture is
  logged as a re-check.
- **Vintages.** A new vintage is created only when a value or its metadata changes for a series and
  period.
- **Runs.** The run identifier is a hash of its inputs, with a unique constraint: the same run twice
  adds nothing.
- **Scenarios.** A set is unique by `(run_id, template_id)`.
- **Workshop queue.** An item is unique by `(card_id, entry_id, trigger kind)`, with a count of
  occurrences.
- **Correction.** A wrong record is never edited. A supersession record points to it, with the
  reason and the replacement.

## Replay

| Kind | What it does | What it must give |
|---|---|---|
| **Deterministic replay** | Recomputes the packet, rules, menu filtering and checks, and reuses the stored model response | The same rows, byte for byte. This is a gate. |
| **Re-pick** | Calls the model again on the same filtered menu | An agreement rate, published as a measure of stability, not a gate. |

Replay and counterfactual runs are stored with their `mode`. Only `live` rows count for scoring and
appear in the export's analysis tables.

## Reference stack

A reference, not a requirement.

| Component | Reference choice |
|---|---|
| Engine | Python |
| Cards and catalogue | YAML, validated by JSON Schema, versioned in Git |
| Capture archive | Content-addressed files (SHA-256) |
| Stores | Append-only Parquet partitioned by `available_at`, queried with DuckDB |
| Menu choices | A hosted language model behind an API, called with a structured-output schema |
| Export | Parquet, shipped with a reader that applies the as-of rule |
