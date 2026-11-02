[Up: Blueprint](README.md)

# Data contracts

## TL;DR

The identifiers, records and rules that let the six layers meet: what a fact, a quantity, a run, an analysis row and a scenario are, field by field.
Time has two axes: when something was knowable in the world, and when Atlas recorded it. Every read is capped on both, so any past run can be replayed exactly.
Every store is append-only and idempotent: the same input twice adds nothing, and a wrong record is superseded, never edited.

## Time

Two axes, both stored as UTC instants.

**World time: when a value became knowable.**

| Field | Meaning |
|---|---|
| `period_start`, `period_end` | The period a value describes, half-open: `[start, end)`. |
| `published_at` | The publisher's official release instant, taken from its calendar: a CPI release at 08:30 New York time is stored as 12:30 or 13:30 UTC. ALFRED's vintage dates are the days FRED updated, which can lag the release, so they are not used for it. |
| `known_at` | The instant from which a value counts as knowable: `published_at` when the publisher or a real-time archive certifies the release, `captured_at` otherwise. For history older than Atlas's first capture of a source with no real-time archive, it is an assumed instant, the end of the period plus the source's declared publication lag, and the record is flagged `point_in_time = false`. |
| `available_at` | On every record: the instant it became available in the world. `known_at` for a fact, `produced_at` for a quantity or an analysis row, `registered_at` for a scenario, `judged_at` for a verdict, `accepted_at` for a card version, `raised_at` for an analyst's flag. |

**System time: when Atlas recorded it.**

| Field | Meaning |
|---|---|
| `captured_at` | When Atlas retrieved the bytes. |
| `entered_at` | When the record entered the store. A backfill entered today about a release of 2003 has `known_at` in 2003 and `entered_at` today. |
| `produced_at` | When a run actually executed. |

**The as-of rule.** A read takes two instants: `as_of`, on world time, and `recorded_by`, on system
time. It returns only records with `available_at ≤ as_of` and `entered_at ≤ recorded_by`. The world
boundary is inclusive: a CPI released at 12:30 UTC is visible to a read as of 12:30 UTC that day, not
to one as of 12:29. A live run reads with `recorded_by = produced_at`, and a replay reads with the
original run's `recorded_by`, so a record entered later (a backfill, a late capture, a correction)
cannot change what the replay sees.

## Identifiers

| Object | Identifier |
|---|---|
| Series | `economy.subject.measure.adjustment.transform`, e.g. `US.PRICES.PCE_CORE.SA.INDEX` |
| Series definition | `series_key@def_version`; a new version opens at a method break, a rebasing, a change of composition (the euro area gaining a member), or a change in what "the policy rate" means |
| Document | SHA-256 of the response body |
| Vintage | `series_key@def_version/period/release_event`, where the release event is the publisher's release (with its `release_stage`: flash, advance, second, third, annual, benchmark) or a capture that found a change |
| Card version | `card_id@version`, fingerprinted by SHA-256 of the canonicalised file, so reformatting does not change the fingerprint |
| Theory catalogue | `catalogue@version` |
| Run | SHA-256 of `(subject, as_of, recorded_by, values_as_of, card fingerprints, catalogue version, engine version, model, prompt version, mode, attempt)`; `attempt` numbers re-picks |
| Quantity | `run_id/quantity_id/period` |
| Row | `run_id/decision_kind/card_entry_id`, or `run_id/residual/residual_kind/subject_key` for a residual |
| Scenario set, branch, verdict | `run_id/template_id`, `…/branch_id`, `…/branch_id/judged_at` |

## Records

**Fact.** `series_key, def_version, period_start, period_end, value | absence_type, unit,
release_stage, kind (observation | forecast, with its forecaster), published_at, known_at,
captured_at, entered_at, doc_fingerprint, anchors[], source, redistribution (allowed | restricted),
point_in_time` (false for history that existed before Atlas's first capture of a source with no
real-time archive).

**Anchor.** `doc_fingerprint, decode_path, byte_start, byte_length, expected_text`. The decode path
reaches inside a container (`zip:xl/worksheets/sheet1.xml`, a PDF content stream); offsets count in
the decoded bytes. A check verifies the document's fingerprint first, then re-reads the range.

**Card version.** `card_id, version, fingerprint, accepted_at, audit_record, test_result`. A card is
visible to a run only once accepted.

**Run.** `run_id, subject, as_of, recorded_by, values_as_of` (equal to `as_of` except in a revision
replay), `produced_at, mode (live | replay | counterfactual), engine_version, card_fingerprints[],
catalogue_version, model_id, prompt_version, sampling_parameters, packet_fingerprint`. A run is
`live` only if it started within a declared tolerance of its `as_of`.

**Quantity.** `run_id, quantity_id, period, value | absence_type, display_precision, input_facts[]`
(each a vintage identifier). The verifier re-reads the input anchors and recomputes the value with
the closed operations before a page may print it.

**Analysis row.** `row_id, run_id, decision_kind (situation | lens_reading | baseline_reading |
menu_pick | scenario | analogue | abstention | residual), decided_by (rule | auto | model | analyst |
abstained), card_entry_id, claim_kind, payload, available_at`. A menu pick also stores the option ids
offered, the rendered prompt and the raw response. `auto` is a menu left with a single option: it
still passes the confirm conditions, and counts with `rule` in coverage.

**Analyst flag.** `flag_id, row_id or subject_key, raised_at, analyst, kind, text_ref`. Its own
append-only record: a flag raised after a run never changes that run's rows.

**Scenario branch.** `branch_id, set_id, lens_id, horizon, trigger, invalidation, outcome_definition,
reference_vintage, trigger_vintage, target_vintage (first_release | release_stage |
latest_at_judgement), discriminating_observable, probability, calibrated (bool), registered_at,
judgement_date, max_release_delay`. When the trigger fires, the branch receives a
`benchmark_probability` computed as of that instant, stored with it.

**Verdict.** `branch_id, state, judged_at, vintages_read[], evidence_rows[]`.

**Supersession.** `supersedes, replacement, reason, entered_at`. It acts on system time: a read with
an earlier `recorded_by` still sees the original record.

## The read

There is one read function, and every layer and the export go through it:

```
read(series_key, periods, as_of, recorded_by,
     vintage = as_of | first_release | stage(s) | nth(n) | values_as_of(t2))
```

Whatever the vintage selector, the result is capped by `as_of` and `recorded_by`: asking for the
first release of a period never returns a value known after `as_of`. One exception, allowed only in
`replay` and `counterfactual` mode: `values_as_of(t2)`, with `t2` later than `as_of`, returns the
values as known at `t2`, **for the periods already released by `as_of`**. That is what a revision
replay reads: the same periods the original report saw, with their later values.

Before Atlas's first capture of a source with no real-time archive, the read returns values flagged
`point_in_time = false`, placed in time by their assumed `known_at`. Only a card's historical
calibration and out-of-sample test may use them, and their results say so; live runs, scoring and
the export's backtest reader refuse them.

## Idempotency and correction

- **Capture.** A document whose fingerprint is already archived is not stored again; the capture is
  logged as a re-check.
- **Vintages.** Every release event creates a vintage, even when it confirms the previous value (a
  third estimate equal to the second is still the third estimate). A capture outside a release event
  creates one only when a value changes.
- **Runs.** The run identifier is a hash of its inputs, `recorded_by` and `mode` included, so a replay
  never collides with the live run it replays. Live runs are also unique by `(subject, as_of,
  engine_version)`: a second live run for the same subject and date is refused, not added.
- **Scenarios.** A set is unique by `(run_id, template_id)`, and is registered inside its run's
  transaction.
- **Workshop queue.** Each occurrence is an event; an item is the group of events with the same
  `(card_id or subject_key, entry or residual kind, trigger kind)`, and its count is derived.
- **Correction.** A wrong record is never edited. A supersession record points to it, on system time.

## Replay

| Kind | What it does | What it must give |
|---|---|---|
| **Deterministic replay** | Reads with the original `as_of` and `recorded_by`; recomputes the packet, rules, menu filtering and checks; reuses the stored model and analyst responses | The same payloads, row for row (run identifier, mode and `produced_at` aside). This is a gate. |
| **Re-pick** | Calls the model again on the same filtered menu | An agreement rate, published as a measure of stability, not a gate. |
| **Revision replay and counterfactual** | Reads with `values_as_of(t2)`, or with one input changed; reuses the original pick where its option is still offered, and abstains otherwise | Rows in `replay` or `counterfactual` mode, never mixed with live analysis. |

Only `live` rows count for scoring and appear in the export's analysis tables.

## Reference stack

A reference, not a requirement.

| Component | Reference choice |
|---|---|
| Engine | Python |
| Cards and catalogue | YAML, validated by JSON Schema, versioned in Git |
| Capture archive | Content-addressed files (SHA-256) |
| Stores | Append-only Parquet partitioned by `available_at` and `entered_at`, queried with DuckDB |
| Menu choices | A hosted language model behind an API, called with a structured-output schema |
| Export | Parquet, shipped with a reader that applies the as-of rule |
