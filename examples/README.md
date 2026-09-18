# Examples

Two things you can look at without taking the main page on trust.

---

## 1. Check the provenance claim yourself

Atlas claims that every number keeps a pointer to the exact bytes it was read from. This folder
holds a real case, not a fixture:

| File | What it is |
|---|---|
| `worldbank-gdp-usa.json` | The document captured from the World Bank API — 1 567 bytes, unmodified |
| `anchored-line.json` | The record Atlas stored after reading it — 30 fields, including the byte offsets |
| `verify_anchor.py` | 72 lines that re-read those byte ranges and check they still hold the stored values |

```bash
python3 examples/verify_anchor.py
```

Output:

```
document : 1567 bytes captured on 2026-07-26
record   : rejeu-positif-worldbank-gdp-usa|NY.GDP.MKTP.CD|USA|2024

  offset  246, length 14  ->  29298013000000         the value itself
  offset  133, length 19  ->  "GDP (current US$)"    series label
  offset  108, length 16  ->  "NY.GDP.MKTP.CD"       series identifier
  offset  218, length  5  ->  "USA"                  country
  offset  231, length  6  ->  "2024"                 reference period

OK: every anchor still resolves.
```

Change one character in `worldbank-gdp-usa.json` and the script exits non-zero. That is the whole
mechanism, in a form small enough to read in a minute.

The script also prints the four timestamps the record carries — when the source published, when
Atlas captured, what the value was known to be at that moment, and the as-of date of the store
entry. That is the point-in-time axis as fields rather than as a design claim.

**Scope.** This is a trimmed standalone extract of the third step of the chain
(capture → anchor → re-read). The full version runs inside the validation suite in the private
repository, against the whole store.

---

## 2. Read a real generated page

[`generated-page.md`](generated-page.md) is the actual output of the report engine, copied
unchanged, with an English walkthrough.

It is short — the store holds 7 records today — and it says so itself. It also names which of its
own choices are hand-made, and the plan item that will make the engine refuse to run until those
choices are derived rather than picked by a human.
