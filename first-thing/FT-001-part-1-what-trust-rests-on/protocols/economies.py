"""Economies' codes for FT-001's coded lists: every source's country name to one ISO 3166-1 alpha-3 code.

The World Bank's list of economies (frozen at ``data/worldbank/_economies/2026-09-30/``) gives the codes and
the first spelling; ``ALIASES`` gives each other spelling the acts' sources use (the Bank of Canada–Bank of
England database, Reinhart and Rogoff's *Varieties* sheet names and *This Time Is Different* issuers, the
chronologies). Economies that no longer exist take their former ISO 3166-3 code (M3's protocol, section 1).
:func:`code` refuses a name it does not know, so no row is dropped or guessed silently.
"""

from __future__ import annotations

import json
from functools import cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
WB = ROOT / "data" / "worldbank" / "_economies" / "2026-09-30" / "page-001.json"

#: Former states and places the World Bank's list lacks (ISO 3166-3 former codes, or ISO 3166-1 codes).
EXTRA = {
    "YUG": "Yugoslavia", "SUN": "Soviet Union", "CSK": "Czechoslovakia", "DDR": "German Democratic Republic",
    "SCG": "Serbia and Montenegro", "ANT": "Netherlands Antilles", "AIA": "Anguilla", "MSR": "Montserrat",
    "COK": "Cook Islands", "TWN": "Taiwan",
    "YAR": "Yemen Arab Republic (North Yemen, to 1990; no ISO code of its own: the workshop's)",
    # The panel (FT-001-M3-panel.md, R1): South Yemen's ISO 3166-3 code, and the euro as one money from 1999.
    "YMD": "Yemen, People's Democratic Republic (South Yemen, to 1990)",
    "EMU": "Euro area (the euro, one money from 1999-01)",
    # FT-001 M4 (war.py): the Correlates of War state system's one state with neither an ISO 3166-1 nor a
    # 3166-3 code that a coded panel also needs (Meissner's table); ISO's user-assigned range (M4 section 1)
    "XAH": "Austria-Hungary",
    # FT-001 M4 frame a (FT-001-M4-frame-a.md, section 1 and Q8): the Straits Settlements have neither an ISO 3166-1
    # nor a 3166-3 code; ISO's user-assigned range (XAA-XZZ) gives XSS, printed in the list's manifest
    "XSS": "Straits Settlements",
}

#: Each source's spelling, lower-cased, to its code. The Bank of Canada–Bank of England database carries
#: "USSR/Russian Federation" as one line: coded on the Russian Federation, which took over the Soviet
#: Union's debt (its note in the acts list says so).
ALIASES = {
    # Bank of Canada–Bank of England database, 2025 edition
    "anguilla": "AIA", "bahamas": "BHS", "bosnia & herzegovina": "BIH", "cook islands": "COK", "curaçao": "CUW",
    "czechoslovakia": "CSK", "côte d’ivoire": "CIV", "dem. rep. of congo (kinshasa)": "COD", "egypt": "EGY",
    "iran": "IRN", "korea, democratic people's republic of (north)": "PRK", "laos": "LAO", "micronesia": "FSM",
    "nauru": "NRU", "netherlands antilles": "ANT", "puerto rico": "PRI", "rep. of congo (brazzaville)": "COG",
    "sint maarten": "SXM", "somalia": "SOM", "st. kitts & nevis": "KNA", "syria": "SYR",
    "são tomé and príncipe": "STP", "the gambia": "GMB", "trinidad & tobago": "TTO", "turkey": "TUR",
    "ussr/russian federation": "RUS", "venezuela": "VEN", "vietnam": "VNM", "west bank & gaza": "PSE",
    "yemen": "YEM", "yugoslavia": "YUG", "eswatini (swaziland)": "SWZ",
    # Reinhart and Rogoff, Varieties (sheet names)
    "centralafricanrep": "CAF", "costarica": "CRI", "cotedivoire": "CIV", "dominicanrepublic": "DOM",
    "elsalvador": "SLV", "korea": "KOR", "taiwan": "TWN", "uk": "GBR", "us": "USA",
    # Reinhart and Rogoff, This Time Is Different, external default dummies (issuers)
    "antigua&barbuda": "ATG", "bosnia&herzegovina": "BIH", "cape verde": "CPV", "congo (brazzaville)": "COG",
    "congo (kinshasa)": "COD", "czech republic": "CZE", "gambia": "GMB", "macedonia": "MKD",
    "north korea": "PRK", "russia": "RUS", "sao tome & principe": "STP", "serbia and montenegro": "SCG",
    "st kitts & nevis": "KNA", "turkey/ottoman empire": "TUR",
    # Garriga (2025), where her two-letter ISO column is empty
    "antigua & barbuda": "ATG", "bosnia-herzegovina": "BIH", "cayman": "CYM", "congo, republic of": "COG",
    "kyrgyzstan": "KGZ", "palestine/west bank and gaza": "PSE", "saint lucia": "LCA",
    "saint vincent and the grenadines": "VCT", "slovakia": "SVK", "sudan, south": "SSD", "swaziland": "SWZ",
    "ussr": "SUN", "yemen, north/yemen arab rep.": "YAR",
    # The panel (FT-001-M3-panel.md): Reinhart and Rogoff's inflation and debt sheet names
    "newzealand": "NZL", "southafrica": "ZAF", "srilanka": "LKA",
    # Ilzetzki, Reinhart and Rogoff's fine classification, its two-row country names joined
    "azerbaijan rep. of": "AZE", "the bahamas": "BHS", "bahrain kingdom of": "BHR", "central african rep.": "CAF",
    "china, pr": "CHN", "congo dem. rep. of": "COD", "congo rep. of": "COG", 'cote d"ivoire': "CIV",
    "czech rep.": "CZE", "guinea bissau": "GNB", "hong kong": "HKG", "kyrgyz rep.": "KGZ", "lao dem. rep.": "LAO",
    "liechtesntein": "LIE", "macao": "MAC", "macedonia fyr": "MKD", "png": "PNG", "serbia, rep. of": "SRB",
    "st vincent & grenadines": "VCT", "syrian arab rep.": "SYR", "trinidad tobago": "TTO", "uae": "ARE",
    "yemen rep. of": "YEM",
    # Correlates of War, state system membership v2024 (FT-001 M4, war.py); "Congo" (ccode 484) is left to
    # war.py's own table, where a global alias would silently catch another source's "Congo"
    "united states of america": "USA", "german federal republic": "DEU", "ivory coast": "CIV",
    "democratic republic of the congo": "COD", "yemen arab republic": "YAR", "yemen people's republic": "YMD",
    "south korea": "KOR", "brunei": "BRN", "east timor": "TLS", "federated states of micronesia": "FSM",
    # FT-001 M4 frame a's hand files (Meissner's Table 1 and Bernanke and James's Table 2.1 as printed; Q8): the
    # names of the period take the ISO code of the economy that bears the name today
    "salvador": "SLV", "siam": "THA", "santo domingo": "DOM", "persia": "IRN", "rumania": "ROU",
    "romania (rumania)": "ROU",
}

#: Rows of a source that are not an economy (totals), skipped by name.
NOT_ECONOMIES = {"total (in sample)", "total (out of sample)", "total (all countries)", "world"}


@cache
def _names() -> dict[str, str]:
    entries = json.loads(WB.read_text())[1]
    # the World Bank's aggregates (regions, income groups, "World") are not economies (M3's audit, M5)
    names = {e["name"].lower(): e["id"] for e in entries if e["region"]["value"] not in ("", "Aggregates")}
    names.update({v.lower(): k for k, v in EXTRA.items()})
    names.update(ALIASES)
    return names


def known_codes() -> set[str]:
    return set(_names().values())


def code(name: str) -> str | None:
    """The economy's code; None for a total row; KeyError for a name no table knows."""
    key = " ".join(name.split()).lower()
    if key in NOT_ECONOMIES:
        return None
    return _names()[key]
