#!/usr/bin/env python3
"""Re-read the byte ranges Atlas recorded, and check they still hold the stored values.

This is a standalone extract of the third step of the Atlas chain
(capture -> anchor -> re-read). The full version lives in the private repository and runs as part
of the validation suite; this file is trimmed to what one person can read in a minute, and it uses
real data, not a fixture:

  worldbank-gdp-usa.json   the document captured from the World Bank API (1 567 bytes, unmodified)
  anchored-line.json       the record Atlas stored after reading that document

The point of the exercise: the record does not merely say "GDP 2024 was 29 298 013 000 000". It
says which bytes of which document say so. That claim can be checked without trusting Atlas.

Run:  python3 examples/verify_anchor.py
Exit code 0 if every anchor still resolves, 1 otherwise.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ICI = Path(__file__).resolve().parent

# Each field of the record carries its own (offset, length) into the captured document.
# The private repository names these fields in French; the English gloss is given here.
CHAMPS = [
    ("value", "offset", "longueur", "the value itself"),
    ("libelle", "offset_libelle", "longueur_libelle", "series label"),
    ("indicateur", "offset_indicateur", "longueur_indicateur", "series identifier"),
    ("pays", "offset_pays", "longueur_pays", "country"),
    ("reference_period", "offset_periode", "longueur_periode", "reference period"),
]


def main() -> int:
    octets = (ICI / "worldbank-gdp-usa.json").read_bytes()
    ligne = json.loads((ICI / "anchored-line.json").read_text(encoding="utf-8"))

    print(f"document : {len(octets)} bytes captured on {ligne['capture_time'][:10]}")
    print(f"record   : {ligne['ligne_id']}\n")

    fautes = 0
    for champ, cle_offset, cle_longueur, glose in CHAMPS:
        offset, longueur = ligne[cle_offset], ligne[cle_longueur]
        relu = octets[offset:offset + longueur].decode("utf-8")
        # The stored value is a number or a bare string; the document holds it with JSON quoting.
        attendu = str(ligne[champ])
        accord = relu == attendu or relu == f'"{attendu}"'
        print(f"  offset {offset:>4}, length {longueur:>2}  ->  {relu:<22} {glose}"
              f"{'' if accord else '   MISMATCH, expected ' + attendu}")
        fautes += not accord

    print()
    if fautes:
        print(f"FAIL: {fautes} anchor(s) no longer resolve to the stored value.")
        return 1

    print("OK: every anchor still resolves. Change one character in the captured")
    print("    document and this check fails, which is the whole point.")
    print()
    print("The same record carries four timestamps, which is the point-in-time axis:")
    print(f"  source published   {ligne['source_published_at'][:10]}")
    print(f"  Atlas captured     {ligne['capture_time'][:10]}")
    print(f"  known to be true   {ligne['known_at'][:10]}")
    print(f"  store entry as of  {ligne['as_of'][:10]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
