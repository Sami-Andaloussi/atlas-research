# ft001-boards — reconstructed dataset

FT-001's currency boards: one line per period during which a money was issued under a currency board, as
Ilzetzki, Reinhart and Rogoff's country chronologies print it. It is the hand list that the panel protocol's
section 7 asks for (c7 (i)): from 16 August 1971, a lagged class 2 ("pre-announced peg or currency board") is
convertible at entry only under a board. It was built under the coders' protocol
`bank/maps/FT-001/missions/FT-001-M3-boards.md`, committed alone (6b709f4) before any board was coded. Frame c
reads it through `strain.board_at` (committed before this list, cf380fc). **The list counts no outcome.**

## Sources

- Ilzetzki, Reinhart and Rogoff, country chronologies, NBER Working Paper 23135 (February 2017), frozen at
  `data/irr/country-chronologies-1946-2016/2026-09-30/`. It was read to October 2016, every country's table
  whole, in page order. PDF page N is printed page N − 1, and each locator gives both.

## Steps

1. The protocol was committed alone (6b709f4). Before it was written, the session had counted the phrase
   "currency board" in the text (33 hits) and read thirty of those lines (dates, classification, a few words of
   comment). It had also counted the frame c lines waiting on this list (120, whose lagged class is 2 at an entry
   from 1971), and read no outcome.
2. Two coders (Sonnet agents, isolated) each read the whole document in page order, and then searched for
   "board" as a safety net, which found nothing new. Neither saw the other's lines or any frame c line. Their
   files are kept verbatim in `coders/`.
3. Agreement (`agreement.json`) is measured on country-years from 1946 to 2016: a board in force on 31 December
   or not (B5's reading, `strain.board_at`), over the 18 moneys either coder listed, 1,278 country-years, 330 of
   them under a board. Both coders listed the same 31 periods, with identical dates and labels, so
   **κ = 1.00**.
4. The differences were settled by the protocol's text, and `series.csv` is coder 1's file with these
   settlements:
   - Bosnia's locator dash and Brunei's quote are cosmetic; coder 1's are kept.
   - Estonia, 1999–2010: coder 2 wrote the anchor "Euro", but no anchor is printed for that period. The column
     is "as printed", so it is empty.
   - Estonia, 1992–94, "Peg (/Currency board)/Freely falling", with a stray slash: both coders read it as a
     board with a second label (B1), and so does the list.
   - Kuwait, 1961–69, "Dual Market/Currency board": the classification names a board as a second label. B1 says
     "alone or with a second label", so it is a board.
   - Trinidad and Tobago, 1935–64: only the comment names the "British Caribbean Currency Board", which the
     country left in 1962. This is a B2 line, in the variant only, with its period as printed. It touches no
     entry from 1971.
5. Not listed, by both coders and by B2's text: the East Caribbean rows (their money is "issued by the East
   Caribbean Monetary Authority", which the text never calls a board), Djibouti, Sierra Leone (the West African
   pound under a row with no board named) and the Comoros (a currency union).

## Assumptions

- B1–B5 of the protocol. B3 is read in code (`strain._first_day`, `strain._end_exclusive`) as follows:
  - a start is the first day of its precision;
  - an end given to the day is the switch date;
  - an end given to the month or the year runs through that month or year, as the chronologies print
    consecutive periods ("April 1994–April 1995", then "May 1995–").
- An empty `end` runs to October 2016. Past it, frame c carries October 2016's state and flags the line
  `board_carried`.
- `period` is the start and `value` is 1, the reconstructed format's required columns.

## Uncertainty

- **31 lines**: 30 boards by their classification (B1) and 1 by a comment only (B2). They cover 18 moneys:
  ARG, BIH, BRN, BGR, EST, GMB, GHA, HKG, KWT, LTU, MAC, MWI, MUS, NGA, LKA, ZMB, ZWE (B1) and TTO (B2).
- **Three `judgement` lines**: Estonia 1992–94 (the stray slash), Kuwait 1961–69 (a board as a second label)
  and Trinidad and Tobago (B2).
- Boards before 1971 are listed for completeness. Frame c reads them only from 1971 (before that, frame a's
  lists decide).
- The chronologies stop in October 2016. A board that ended later, or began later, is not seen.
- The list rests on the chronologies' own labels. A board that the chronology classifies otherwise (Djibouti,
  whose franc is often described as board-issued) is not a board here. This is said, and no other source is
  added round the protocol.
