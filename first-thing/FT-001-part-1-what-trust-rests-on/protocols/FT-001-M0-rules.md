# FT-001 — M0: the rules, fixed before any case is coded

> Mission M0 of `bank/dossiers/FT-001-the-life-of-a-money.md` (section 14, "Effort"). **Version 4.2**,
> 2026-09-30, written by the E2 session (`plan/e2-ft001.md`). Version 1 was commit 2990473, audited in
> `bank/checks/FT-001-M0-2026-09-30-opus-audit.md` (not yet: B1, O1–O17, M1–M11; answers bracketed
> [a-…]); version 2 was commit ff44bbe, audited in `bank/checks/FT-001-M0-2026-09-30-opus-audit-2.md` (not
> yet: B1, B2, O1–O7, M1–M16; answers [b-…]); version 3 was commits 7cdb4bb and 288b6b6 (edited once
> before any coding, two pair hashes — the YAML's parent block names both) [c-M1], audited in
> `bank/checks/FT-001-M0-2026-09-30-opus-audit-3.md` (not yet: B1, O1–O10, M1–M17; answers [c-…]); version 4
> was commit 3a1727a, read by a narrow check, `bank/checks/FT-001-M0-2026-09-30-opus-narrow-check-v4.md`
> (round 3's findings done, the guards table since; **A11 not yet: a B**; O1–O5, M1–M11; answers [d-…],
> the check's Question 1 [d-Q1]). **Version 4.1** (commit 5b95936) **changed no decision rule**: it wrote
> the check's B in section 10 as declared — step 8 allows no fifth round of design —, corrected the grid
> answers that claimed a guard A11 does not have, answered the grid's sixth question (section 8) by
> declaring, and aligned the twin and frame f with the prose and A10; it **added one hold** (no bank read
> for A11 until Sami answers), **one variant** (A11 with First Republic in) and **one duty** (claim 2's
> smallest detectable effect printed for the rule as written before any count). Its small audit,
> `bank/checks/FT-001-M0-2026-09-30-sonnet-small-audit-v41.md` (no B; O1–O5, M1–M9), is answered here,
> **version 4.2**, again with no decision rule changed [e-…].
> **Step 8 of `ft-map`**: after round 2, claim 1 was told (two rounds, one kind of hole). **Round 3 is the
> third round with a B**: M0 goes forward with that B declared in its holes (section 10) and put to Sami,
> with no fourth round of design. Its B1 (claim 2's count carries the state's default, fiscal distress
> the matching did not hold) is answered by **the auditor's own repair, simulated there at 0–3% false
> confirmations** (section 6, claim 2) — written, not re-audited in depth. Claim 3 is told for the data
> M3 found. **A11 is tested again** on its model's version of 5 April 2023, the earliest that can be had
> (section 7) [c-M14]; the narrow check finds it can confirm with no effect: declared, and **no bank is read
> and no A11 verdict computed until Sami decides whether it stays declared or is told** (section 10) [d-B].
> **The lock** [a-O16]: this file and its twin `FT-001-M0-rules.yaml` are hashed together by
> `missions/code/m0.py`; each coding mission (M2–M9) refuses to run unless both are committed and
> unchanged, writes the pair's hash into every coded line, and checks that each coded list was first
> committed after the rules it names, and after the lists the twin says it follows (section 3) [b-M13,
> c-M2]. A changed rule is a new version, committed before any case it touches is coded; **no list is
> coded under v3 or v4** [c-M15].
> **What was seen before writing**: the dossier, its maps, the guards table, the three dossier checks,
> M0's three audits and their simulations, the pilot's cards C05, C09, C11, C12 and C15 and its `STATE.md`,
> D1's licence decisions, the coverage of M3's two batches of frozen sources (which series exist, for
> which years and economies — no value), and two facts the third audit read and printed: the world counts
> of sovereigns with a stock in default (a separator's prevalence, 36 of 157 in 1970 to about half after
> 1990) and the pound's 1975 inflation in Thomas and Dimsdale's series. **No data of any frame of parts
> 1, 3, 4 or 5** — no price, act, deposit or flight measure of a case — has been read.
> **Not redone here**: frame e, A4, A5, A6 and part 2's door are the pilot's (E1), in its cards
> (`studies/FT-001-part-2-where-printed-money-goes/cards/`); M0 cites them where another frame reuses
> them. **The pilot's regime rule** (the IFS ±2% band) governs part 2's A5; **M0's** (section 1) governs
> parts 1, 3, 4 and 5 [a-M9].
> **Where M0 departs from the dossier**: section 9 lists every departure; each goes into the map's change
> log and the dossier once M0 is written in them.

## 1. Common definitions

- **A money** — a unit of account issued under one authority, with its own price level. The euro area
  is one money from 1 January 1999; its members' monies before are their own. A new unit is **a new
  money** (the old money's life ends "broke, replaced") if it is introduced while the old money is broken
  (section 5 b) or within 24 months of its restoration; otherwise the old money is chained through the
  new unit at the conversion rate [a-O12].
- **Convertible** — redeemable on demand by any holder, at a stated rate, into metal or another money.
  **Parity** — the legal or official rate, redeemable or not. **Two prices** — a quoted agio or a
  parallel market rate against that parity, while it stands. A money with no parity has no "two prices".
- **Regime at a date** [a-O10, b-M1] — Ilzetzki, Reinhart and Rogoff's **fine** class 12 months before the
  date, from the file frozen by M3 (1946–2016): *a parity* = classes 1–10 (no separate legal tender,
  boards, pegs, crawling pegs, and announced or de facto bands — class 9, an announced crawling band of
  ±2% **or wider, with no upper bound**, included: an announced band is a commitment whose abandonment is
  an announced act; variant: class 9 read as floating); *floating* = 11–13; class 14 ("freely falling")
  is defined by inflation, an outcome, and is never used — the last class before it stands; class 15 (a
  dual market, parallel data missing) = a parity whose premium cannot be read. **After 2016** the 2016
  class is carried forward, flagged, and a variant drops those years (the 2017–2019 update is only on
  `www.ilzetzki.com`, a wall; should it open, it enters by a new version). Before 1946, the gold-standard
  lists of frame a.
- **Inflation** — π12(t), the 12-month change of the consumer price index where a monthly index exists;
  else π(y), the change of the year's average. **Its rise** — Δπ over 1 year and over 3 years.
- **Depreciation** — d, the change over 12 months of the rate against the dollar or the money's anchor
  (Reinhart and Rogoff's currency-crash definition) [a-M1]: **the market rate** under a floating regime,
  **the official rate** under a parity (a devaluation within a kept peg is value, section 2) [b-B2];
  **its acceleration**, Δd over 1 and 3 years. **The premium** — 100·(parallel/official − 1) while a
  parity stands; Δp over 1 and 3 years. **No open parallel-rate series was found** (Reinhart and Rogoff's
  *Exchange Rates (Official and Parallel)* is named on their site with no file; M3): the premium's level
  is read only where a parallel series is found by hand (a variant, reported by source); in the headline,
  **"two prices" is the existence of a dual, multiple or parallel market** — Ilzetzki, Reinhart and
  Rogoff's dual-market dummy at 1 (0 = unified) [c-M10], or class 15 — while a parity stands [b-M16].
  **Reserves** — the central bank's reserves less gold, in dollars (IFS `RAXG_USD`); their change over 12
  months.
- **Sources, in a fixed order** [a-O17] (the first with data for the money-period is used; a seam between
  sources is flagged, never smoothed): **prices** — IMF IFS, World Bank, Reinhart–Rogoff, the BIS's long
  series, Jordà–Schularick–Taylor; **debt** — the IMF's Historical Public Debt Database (the DBnomics
  mirror of its 2016 vintage, to 2015), the IMF's World Economic Outlook (general government gross debt,
  DBnomics, from 1980), Reinhart–Rogoff, Jordà–Schularick–Taylor; **deficits** — the World Economic
  Outlook (from 1980), Jordà–Schularick–Taylor; **central-bank credit to the state** — IFS (line 12a to
  2000; `FASAG` from 2001, the seam flagged); **money** — IMF IFS, Jordà–Schularick–Taylor; **exchange
  rates** — IMF IFS, Reinhart–Rogoff; **market structure** — Ilzetzki–Reinhart–Rogoff; **debt in own
  money** — Reinhart–Rogoff's domestic and external public debt where both exist (to about 2010), after
  which it *cannot be read*, never assumed [c-M17]. **Mauro et al.'s
  *Public Finances in Modern History* is not in the order**: the IMF's site refuses the toolkit's client
  (M3, "Walls met"); should it become readable, it enters by a new version, never silently [b-M16].
  **The Global Macro Database is not used** (its terms bar use inside a company; D1, Sami's answers).
  Where Jordà–Schularick–Taylor only compiles a public series, a published chart is drawn from the public
  series (C2 Decisions, Sami's answer 4).
- **A source's last year** [b-M16] — a money-period past the last year of the source that dates an item
  (an act, a regime, a premium, a debt ratio) is **cannot be read** for that item, **never "none"**: L2
  and H1 after September 2016 (the chronologies' end), T2's external dummy after 2014 where the Bank of
  Canada–Bank of England database does not reach, and every parallel premium where no series exists.
- **The panel's common end** — as the pilot's C05: monthly, the last month in which at least half of the
  monies that had a price index twelve months earlier still have one; annual, the last year in which at
  least half of the monies that had one the year before still have one.
- **Eras** — *metal*, to 31 July 1914; *gold exchange and Bretton Woods*, 1 August 1914 to 15 August 1971;
  *fiat*, from 16 August 1971. Before 1800, frame d only.
- **War, the common cause** [a-O9] — a war year for a state is one in which (a) at least 1,000 battle
  deaths fell on its territory (UCDP by location from 1989 where open, else the World Bank's battle-deaths
  series; the Correlates of War's intra-state wars and the interstate wars fought on its soil before), or
  (b) it took part in a Correlates of War war in which its own forces lost at least 1,000. **A case
  entering in a war year is apart**; war **inside** a horizon or window is coded, never apart. Fiscal
  emergency is measured, not coded apart: it is frame c's strain — **its route and the tercile of the
  route's measure** — a stratum wherever pressure is stratified (section 6) [b-B2, b-O7].

## 2. The supports, and the acts by which each gives way (closed lists)

A support **stands** at a date if its condition below holds then. It **gives way** only by a dated act
from its list; nothing else counts as giving way (a falling share of payments, a rising premium, a run,
a devaluation within a kept peg — those are trust and value, the outcomes) [a-O3]. A new support can be
added only by a new version of this file.

**The currency** — the **headline acts** are those with a headline source; the others are variants,
reported by source [a-O3].

| Support | Stands when | Acts that make it give way | Headline source |
|---|---|---|---|
| *Taken back* — the issuer takes its money back and honours its own claims | legal for taxes, and the state not in default (a stock in default in the Bank of Canada–Bank of England database; Reinhart–Rogoff before 1960) — this condition carries fiscal distress, so wherever the support is counted, default at entry is also held (below) [c-B1] | T1 taxes required in metal, another money or kind · **T2** a default or restructuring of the state's debt, external or domestic (its year) | T2: Reinhart–Rogoff's *Varieties* to 1959 (domestic and external; for the M–S countries, whose file is missing, the external dummy of *This Time Is Different*, domestic defaults cannot be read); the Bank of Canada–Bank of England database from 1960 (stocks in default by year: the year of a default is the first year of a stock). T1: hand, variant |
| *Redemption* | convertible | R1 convertibility suspended · R2 the parity changed while convertible | frame a's lists (claims 1 and 5 count inconvertible monies) |
| *A limit on issue, by rule* — a statutory cap, a peg, a currency board | one of them in force — a statutory cap: Garriga's lending-limits component (`cuk_limlen`) at or above **0.5** [0.25; 0.75] (a convention, the scale's midpoint) [c-O10] | **L1** a statutory cap on issue or on central-bank credit to the state lifted or raised — a year in which `cuk_limlen` falls (the component moves only with the statutes Garriga codes) [c-O10] · **L2** a peg, band or board **abandoned** by an announced decision (dated by the announcement in Ilzetzki–Reinhart–Rogoff's chronologies, to September 2016); a change of de facto class with no announcement is value, never an act | L1: Garriga's lending-limits component (1970–2023); L2: the chronologies (1946–2016). Variants: a devaluation of 10% or more within a kept peg; a step beyond an announced crawl |
| *A limit on issue, by institution* — central-bank independence, an inflation target | Garriga's index at or above **0.5** [0.4; 0.6] (a convention, the scale's midpoint), or a target announced | **L3** a legal reform Garriga codes as **decreasing** independence (her `reform` and `decrease` flags), or a target abandoned; variant: the index down by **0.05** or more [0.03; 0.10], a convention [c-M3] | Garriga (1970–2023); targets as frame a |
| *Habit* | sole legal tender | **H1** another money made legal tender or legal for domestic contracts, by an announced decision | the chronologies (to 2016) |
| *Force* — legal tender enforced, controls, bans | Chinn–Ito's ka_open at or below **0.25** [0.1; 0.5] (the index's lowest quarter), or a ban on residents holding foreign money | F1 controls or a ban lifted, dated by AREAER's text of the change | none open: ka_open smears a change over five years, and AREAER's text is behind a sign-in, so F1 is a variant only; ka_open serves only for "stands" |
| *World demand* | the money is in COFER's reported list (Eichengreen–Chiţu–Mehl before 1999) | W1 a dated decision by an official holder to cut its holdings | hand; a variant only |

*A limit by rule* standing on a de facto class (a peg, a band, a board) stands on the rate's stability,
which is value (Q5): that is why claim 2 is also given without pegs and boards [c-M11].

**The account** (part 4): *cash at par* · *deposit insurance* (an explicit scheme, its limit) · *a lender
of last resort* · *the bank's solvency* · *the state behind it* (its debt, and the share in its own money;
for euro members both readings — the euro as the member's own money, and as not) [a-M5]. At entry these
are separators (A10); after entry, failures, holidays, freezes, nationalisations, forced sales,
guarantees and liquidity support are **dated responses**, described, never separators.

**Force imposed is not a support giving way**: controls, legal-tender penalties or price controls imposed
after strain are claim 5's phase 4, a response, never an act of this list.

**A private issuer's supports** (claim 4, stablecoins), one line each, written before any coin is read
[a-O13]: *redemption* — the terms give holders a right to redeem at par on demand (who may redeem is
recorded: any holder, or verified customers only); *a limit by rule* — issue tied by contract or code to
reserves held one for one, or to a stated cap (a target alone does not count); *a limit by institution* —
the issuer supervised under a law that limits its issue; *taken back* — the issuer accepts the coin for
its own fees or claims; the reserves held at banks rest on *the account's* supports (insurance, the
bank's solvency, the state behind it). A stated mechanism that meets none of these lines lies outside the
list.

## 3. The case line, and the coders

**Every case of every frame is one line** in its coded list (`data/reconstructed/ft001-<frame>/`, whose
`series.csv` keeps the reconstructed datasets' columns — `period` the entry date, `value` the entry
measure, `unit`, `source`, `locator` — beside these):

`money · frame · route · entry_date · entry_measure (value, date) · outcome · outcome_date · onset_date
(frame b) · responses (type:date; …) · exit (competing: type, date, source) · status · source · locator
· coder · rules_sha256`

`status` is one of *counted* · *already under way* · *censored* · *ended unbroken* · *cannot be read* ·
*apart* (with its reason). **The line's check, in code** (`missions/code/m0.py`, run on every coded list
before it is committed): an entry on or after its outcome, or a response dated before the entry, is
refused unless the status is *already under way* or *apart* (an apart line is never counted, and its
reason is written) [b-M12]; a matching measure whose date **ends after the entry's** is refused — an
annual measure for a monthly entry is refused, since the year runs past the month [b-M12]; **a counted
line whose onset (frame b) is not after its entry** is refused — it is *already under way* [c-O6]; a date
that cannot be read is reported, not raised [c-M17]; a line whose `rules_sha256` is not the committed
pair's hash is refused.

**The commit order, in code** [b-M13]: `m0.py` refuses a coded list (a) whose first commit is not a
strict descendant of the commit that fixed the rules' hash its lines name, and (b) whose first commit is
not a strict descendant of the first commit of every list it follows — **the acts list before any
outcome list**: which lists follow which is **declared in the twin** (`case_line.follows`) and read by
`list_problems` itself, so that a check run without a flag cannot skip it [c-M2]. What
the code cannot check: that nobody looked at an outcome before coding the acts — the coders' protocol
below, said, is the only barrier there.

**The coders.** Rules first (this pair, committed); acts coded **before** any outcome of the same frame is
computed, in a separate commit; from the headline sources of section 2, run identically on every
money-year of the frame, never searched case by case. Coders are outcome-aware — the histories are
known — so the headline uses the sources coded for every money; anything found by hand in a monetary
history is a variant, reported by source, with **the act rate by source** for the headline set too
[a-R4]. A second coder (an independent agent) recodes a 20% random sample (seed 1797) of every hand-coded
list; agreement is reported (Cohen's κ); disagreements are settled by the text of this file, never by the
outcome.

## 4. Censoring, and monies that end unbroken

- Only **the panel's common end** censors. A case whose horizon or window runs past it is *censored*:
  reported apart with what happened so far, counted neither way.
- A series that **stops early because of a crisis** (a war, a state ended, a money replaced after a break,
  statistics suspended) is coded from the record by what happened, or *cannot be read*.
- **A competing exit** [R3] — a money that ends by a union, a merger or a replacement unrelated to
  breaking: a dated act announced at least 12 months before the exit, with no crossing of the break line
  in the 12 months before it (the lira, the franc, the drachma into the euro). In a hazard model it
  leaves the risk set at its date; in a fixed-horizon count it is *ended unbroken at h*, apart, and **every
  verdict is given twice** — those cases counted as held, and left out. If the verdict turns on them, "we
  cannot conclude", said.
- A window that **starts before the record** of acts or prices begins is *apart*, never "no act"; a
  window that runs **past a source's last year** reads that source's items as *cannot be read* (section
  1) [b-M16].

## 5. The frames' rules and parameters

Headline value first; the grid, reported whole, in brackets.

- **a. Support changes** (A2). *Panels, by rule*: every money convertible on 31 July 1914 (Meissner's
  gold-standard dates) and its suspension in 1914–15 — the belligerents enter in a war year, so they are
  told and the neutrals counted [a-M3]; every money on gold at the end of 1929 (Bernanke and James's
  table; Wolf's list where wider) and its exit in 1931–36; every legal reform Garriga codes, up or down (her
  `reform` and `direction` flags, 1970–2023; every change of the index of 0.05 or more a variant) [c-M3]; every inflation-targeting adoption (Hammond, the targeters at the start of
  2012; the adopting central bank's announcement after). *Window*: from 3 years before to 5 years after,
  annual [monthly −24 to +36 where monthly data exist]. *Non-changers*: monies with no change of the same
  panel within ±3 years, up to five per change, nearest by π in the year before, within 3 points [1; 5].
  *Apart*: exits after a run — reserves down 20% or more in the 12 months before [10; 30]. *Measured
  apart*: value (π, depreciation, the market split) and trust (deposits to GDP, currency to deposits,
  dollarisation, reserves). Frame a is where part 1's timing is read **forward and counted-free**: each
  change dated, value and trust from three years before.
- **b. Breaks**. *The line*: π at or above **20%** (Reinhart and Rogoff) [40%, Bruno and Easterly; 100%,
  Fischer, Sahay and Végh]. *Crossing*: the first of **3 consecutive months** at or above it [1], or the
  first year whose average is [a-M6]. *Restored*: π below the lower line for 24 consecutive months (2
  years); a crossing after that is a new break. **The pound in 1975** [b-M8]: its annual inflation is above the headline
  line in every series (22.7% in Thomas and Dimsdale's preferred CPI, 24.2% in their RPI-based series;
  frame b reads IFS first) [c-M9], so it enters as a break of a reserve money, restored or not by the rule — **the line is not moved to keep it out or in**; under the 40% grid it is not a
  break, reported. *Onset* [a-O1]: the earliest date from which **one route's measure stayed at or above
  its line up to the crossing** — π at the **lower line, 10%** [5; 15]; the depreciation at **15%**
  (Reinhart and Rogoff) [10; 25 with a 10-point rise in the rate, Frankel and Rose], the market rate under
  a floating regime and the official rate under a parity (no parallel series: section 1); the premium at
  **10%** [5; 25] only where a parallel series is found by hand (a variant) — **provided that run began
  within 36 months of the crossing** [24; 60]; a route whose run began earlier does not date the onset (a
  chronic premium dates nothing). **When no route's run began within the bound** (a slow climb from the
  lower line), the onset is dated **at the bound**, crossing − 36 months, flagged; a variant sets those
  breaks apart [b-O2]. A market split first recorded, or a premium first passing its line, in a month
  (year) when controls were imposed or tightened dates no onset; the inflation-only onset is a variant.
  *The first public crossing* (A12, A13): the release date of the first index reading at or above the
  line.
- **c. Strained monies**. *Routes*, reported apart, **tie order c1 > c2 > c3 > c4** [a-O7]: c1 debt at or
  above **90%** of GDP [60%]; c2 a deficit at or above **3%** of GDP [5%]; c3 central-bank credit to the
  state rising by **50%** or more of the year's deficit [25; 75], with the deficit at or above 3% (from
  1948, IFS); c4 an episode of the pilot's card of record, **C15** (`C15-e-episodes-closed`, hash
  `3bf06edbb0f3c3767191c1d1c63a3c3c70183eb6486ceaddefb149700018d8dc`, commit d58f06f) [b-O1], entering in
  the year of its **crossing c**, from 1950 once C15 has run — its headline list (every one-month jump set
  apart). As the pilot declares [b-O1]: **the narrow card check's O1** — nine lines flagged "likely
  reclassification, unread" (BJ, NE, SN 2003-12; DM, KN, VC 1984-03; DK 2012-07 and 2021-03; GT 2001-12)
  and CI 2001-10→2002-12 through its December-2001 seam enter c4 as they enter C15's headline, flagged; a
  variant drops them; **its O2** — December seasonal spikes still enter the headline; the pilot's
  smoothing variant's list is read beside, a variant. C09 is never read (its check found it faulty); C11
  was replaced by C15. *Entry*: the first year any route is met; **one spell per horizon** — the next
  entry of the same money only after H. *Apart*: π at or above the lower line in the entry year or the
  year before ("already inflating"), **or an entry on or after frame b's onset by any route** — the
  depreciation route included [c-O6] — with the variant counting the entry-year ones as entrants whose
  outcome is read [a-O7, the twin of conf-m10]; convertible at entry (claims 2 and 5); entry in a war
  year. *Outcome over* **H = 10 years** [5; 20]: *broke* (frame b's crossing in any year from entry+1 to
  entry+H) · *held* · *broke and restored* (broke, then restored, the same money, before entry+H).
  *Matching*: within route, by tercile of the route's entry measure in the entry year (terciles of all
  entrants), by era, and **by the state in default at entry or not** (section 2) [c-B1]. *Outside the fitting sample* [b-M8]: the 90% line was fitted by Reinhart and Rogoff
  on their countries to 2009 — route c1's results are reported apart for the years after 2009 and for the
  economies outside their sample; 3% and 50% were fixed, not fitted, and have no fitting sample.
- **d. Debased coins before 1800**. *Entry*: a fall of **5%** or more in a year in the silver (or gold)
  content of the unit of account (Reinhart and Rogoff), from Karaman, Pamuk and Yıldırım-Karaman's
  series. *The one search procedure*, run on every debasement: every Allen–Unger series whose currency is
  that unit and whose place lies in that polity; kept if at least **3** commodities [2; 5] cover **70%**
  [50; 90] of the years **from entry−5 to entry** [a-M4] (conventions fixed before any data) [c-M17]; after entry, gaps are coded by section 4; the index is the median of
  the commodities' log changes. A debasement with no such index is told, never counted; Sami's named
  cases enter only if the procedure finds them. **Karaman et al.'s series cannot be reached today**
  (second batch: CEPR's PDF answers 403, the other copies sit on refused hosts): frame d waits, declared;
  Allen and Unger's table of metal contents is not swapped in.
- **f. Bank distress**. *Routes*: f1 a real total return on bank equity of −30% or worse in a year (Baron,
  Verner and Xiong) that is at least **10 points** below non-financial shares' [0, the unfiltered
  variant; 20]; f2 non-performing loans first at or above **20%** of loans (Laeven and Valencia's line),
  where an annual series exists — never Laeven and Valencia's crisis peak, which the crisis selects
  [a-feasibility]; f3 the state's own default (T2) while banks' claims on it are at least **10%** of their
  assets [5; 20] — a stratum, described, never pooled. *Ordering*: dated at the earliest crossing of any
  route, one episode per country, no new episode within **K = 5 years** [3; 8]; ties: f1, then f2, then
  f3. *Already breaking*: depositors lost money or access on or before the entry date; **on f1 and f2**,
  whose data are annual, a loss in the entry year, with the variant counting those as losses [conf-m10,
  a-O14]. *Outcome within* **3 years** [1; 5]: a loss of money (any cut, conversion or haircut) or of
  access (a freeze, holiday or limit lasting more than **5 business days** [1; 20]) touching at least
  **5%** of system deposits [1; 10], or any cut to insured deposits; the plain yes or no a variant.
  *Matching*: within route, by tercile of the entry measure (the equity return in the crossing year; the
  loan ratio in the entry year), by era [a-M5], and by the state in default at entry or not — A10's
  stratum, which this line had not followed [c-O9, d-M5]. Route f1 waits on Baron, Verner and Xiong's data, which
  Dataverse serves only through a signed URL the toolkit refuses (M3; Engine notes): until then f1
  cannot be read, never swapped.
- **g. Stablecoins — told** [a-O13; D1]. DefiLlama's terms bar the commercial copying of its data (Sami's
  decision, D1), and no open census of coins that includes the dead ones is known, so no coin can be
  entered by rule: frame g is **told**. The coins named in sourced reading are each mapped onto section
  2's private-issuer lines by two coders apart, κ reported, no verdict. *Two prices*: redemption halted,
  gated or limited by the issuer's notice; *broke*: below par by **3%** [1; 10] for **7 consecutive
  days** [1; 30] — used only to date the told phases (A9).
- **h. The investor rule** (A13; **its card is M8's**, as the dossier's section 14 says — M0 fixes only
  the frame's rules [b-M8]). *Signals*: Kaminsky, Lizondo and Reinhart's indicators and percentile
  thresholds, each computed on an expanding window of the country's own data, silent before **60 months**
  of history [36; 120]; the real exchange rate's trend fitted on data to date only (an expanding linear
  trend on its log) [a-O15]; *alarm*: at least **3** indicators signalling in the month [2; 4] **or**
  public debt crossing Reinhart and Rogoff's line (90% of GDP; external debt 60% for emerging economies)
  [joined by "and"; each alone]; on for **24 months**. *Release lags*: monthly 1 month, quarterly 3,
  annual 9 [each doubled]. First-release vintages where they exist (ALFRED; IFS's archived editions).
  *Refuge*: the dollar for a saver in a strained money; gold for a saver in dollars or euros.
  *Benchmarks*: cash, a 60/40 local portfolio where priced, gold held throughout. *Robustness*: a block
  bootstrap of 12-month blocks; each episode left out.
- **i. Today's class**. Frame c's rule applied to the latest complete year, to every money, whatever its
  name; the reserve monies read are COFER's reported list; the euro as a union and member by member.
- **j. The run test** (A11). Every US bank filing a Call Report for 31 December 2022, less SVB, Signature
  and First Republic; the outflow is the change in total deposits to 31 March 2023, as a share of those of
  31 December 2022, also shown beside each bank's uninsured share and its securities' unrealised losses at
  31 December 2022. The Call Reports are FDIC's current database (amended filings, not first filings),
  said. **A bank with no report for 31 March 2023** (merged or failed in the quarter) is left
  out, counted and named; a variant counts a failed one as an outflow of 100% and reads a merged one on its
  acquirer's change [b-M14].
- **k. Flee or stay** (claim 3). *Entry*: **the last year** of a run of **N = 2** years [1; 3] in which the
  real deposit return (the deposit rate less π) is below **−5%** [0; −10] (Gelb; Roubini and
  Sala-i-Martin), so that the entry is known when it is dated [a-O5]; from 1970; one entry per window W.
  The rest is claim 3's (told).

## 6. The claims' decision rules

A counted claim has a margin, a floor for "too thin", and three outcomes: *confirmed*, *refuted*, *we
cannot conclude*. Intervals are 90% intervals from a bootstrap over monies (2,000 draws), since one money
gives several years. **The smallest detectable effect** of each test (80% power, 5% one-sided, on its
counts) is printed beside its verdict [a-R5]; **at the floors, fixed now** [b-M10]: claim 2 and A10 (20
per side, a share near 0.6) detect about **39 points**, four times their margin (computed before claim 2's default stratum and its
reading without "taken back": the narrow check reads the rule as written at roughly half that power, 15–29%
against 29–51% at 0.5 logit per support, so the coding mission prints the rule as written's effect by the
same simulation, on no outcome, before any count [d-M1]); test (i) (20 lives per
group) about **0.27**, near three times its margin; **test (ii)** — the third audit's simulation (160
monies, 40 years, M0's strata measured with noise): the joint rule confirms 7% of runs at a true ratio of
2 per phase and 47% at 3, and refutes 0–1% under no effect, so **test (ii) will in practice end "we
cannot conclude" unless each effect is about twice the margin, and claim 5 can fail only through test
(i)** — said now [c-O8]. **A verdict at a floor confirms only effects several times the margin — said with
it.** The margins (1.5 for ratios, 10 points
for shares) and the floors are conventions fixed before any data, one per kind (plan, Decisions,
"Headline values") [b-M9].

**The pressure strata** — used by claim 5 (ii) and by claim 1's description [b-B2, b-M2]: π (below 5,
5–10, 10 or more); Δπ over 1 and 3 years (≤0, 0–5, above 5 points); d, **for every regime** — the market
rate under a floating regime, the official rate under a parity — (below 5, 5–15, 15 or more) and Δd over 1
and 3 years (≤0, 0–10, above 10); for parities, the market split (a dual or parallel market recorded, or
not); **reserves** over 12 months (a fall of 20% or more, or not) [10; 30]; **strain — frame c's route and
the tercile of the route's measure** (terciles over all strained at-risk years of that route, the measure
read at the date each reading uses) [b-B2 (a), c-M5]; **the state in default or not** [c-B1]; supports standing (one, two or more); the regime; decade.
**Two readings**: **A**, the strata measured up to the end of the year before; **B**, up to the end of the
year itself — A cannot see pressure earlier in the same year, B may take in the effect, so the two bound
the answer [a-B1].

**Claim 1 — told, not counted** [b-B2; `ft-map` step 8]. *Why*: the claim's question — does value fall
after a support gives way, rather than before? — was patched five times (three dossier checks, two M0
audits), and each round found the same kind of hole one step lower: a pressure or a common cause the
strata missed (the onset, the band, the no-rise stratum, same-year pressure and reserves, then fiscal
strain and a parity's official rate). The second audit's simulations, built from M0's own rules, show
that even with strain added the forward test confirms in 1–8% of runs with no effect of any act, and that
its no-rise stratum holds a median of 1–7 exposed onsets, so "we cannot conclude" was the likely outcome
either way. Step 8 says: stop patching. **What part 1 shows instead**:
- *Each break's line*: every break (frame b's crossing) of a frame c counted money from 1970, one line, in
  the order of time — its entry route and tercile, each headline act with its date and source, the
  onset and the route that dated it, the crossing, and in the year before each act: π, d (market or
  official), reserves' 12-month change, the market split, war years.
- *The described shares*: of those breaks, the share whose onset came **after** a headline act (within
  L = 3 years [1; 5]), the share whose onset came **before** the first act in the L years around it, the
  share with an act in the onset's own year, where the order cannot be read by year [b-O3], and the share
  with **no act at all** in the window [c-M7]; beside them, **the base rate on the same window** — the
  share of strained at-risk years with a headline act in the L years before them (not the forward
  table's exposed side, which is an act in the year itself) [d-M4], so that "after an act" is read against how often an act falls in any L
  years without a break [c-O1]. *Strained at-risk years* [b-O4]: the years of a counted spell of frame c, from entry to
  entry+H−1, before any onset in the spell, with π the year before below 10% and at least one support
  standing.
- *The forward table, as a description*: those years as trials — *exposed* if a headline act (T2, L1, L2,
  L3, H1) falls in the year, *unexposed* if none falls in it or the L years before — with an onset in the
  next L years, counted within the pressure strata, readings A and B; each stratum's counts and rates, the
  pooled Mantel–Haenszel ratio, and **the same without T2** (a default is itself fiscal distress) and each
  act alone [b-B2]. Printed with it, in words: *strain and expected inflation are not closed; a ratio
  above 1 here cannot be read as the effect of an act.* No margin, no verdict. War years apart [b-M3].
- *Where timing is read*: part 1's "value falls after a support gives way" is **described, never
  counted** [c-O2] — here, and in frame a (A2, an event study with no verdict: dated changes, value from
  three years before). What claim 5 counts is narrower: the order of phases 2–5 in lives that broke (of
  which only L1 is an act of section 2) and the odds of an onset after each phase.

**Claim 2 — the cross-section** [a-O6, a-M7, b-M11]. Frame c's counted monies over H, **from 1970**
(Garriga and Chinn–Ito measure the supports from then; before, a variant counting *taken back* and *a
limit by rule* only). *Units*: spells, one per money per horizon (section 5 c); *broke and restored*
counts as **not held**. *Separators at entry*: the number of currency supports standing among *taken
back*, *a limit by rule*, *a limit by institution* and *force* (two or more against one or none); each
support alone; debt in own money (half or more of the state's debt in its own currency); a substitute at
hand (claim 3's cells). *Statistic*: the difference in the share *held*, more supports against fewer,
Mantel–Haenszel over the matching strata — route × tercile × era × **the state in default at entry or
not** [c-B1]. **Margin: 10 points.** Confirmed if at least 10 points with its interval above 0; refuted if
the interval lies wholly below 10 points; otherwise we cannot conclude. **Given with and without "taken
back" in the count** — its condition is the state not in default, which is fiscal distress; if the verdict
turns on it, we cannot conclude [c-B1] (the third audit's repair: 0–3% false confirmations in its null,
against 9–59% without it; written from that simulation, not re-audited in depth — section 10).
**Given with and without pegs and boards in "a limit by rule"** — a hard peg, like convertibility, must
give way before a break, the twin of the convertible monies set apart; if the verdict turns on them, we
cannot conclude. Entries after 2016 read the regime carried forward (section 1): **given with and without
them**. Too thin: fewer than 20 counted **spells** on either side [c-M8]. War inside a horizon is coded:
a variant leaves out the spells with a war year inside H [c-M12]. Habit, world demand and reserve status:
variants only.

**Claim 3 — told, not counted** [R2, R5; a-O4, a-O5; b-O5, b-O6, b-M4]. *The question*: where deposits lose
more than 5% a year in real terms, do holders leave the money more where they are free to and have
somewhere to go? *Why told*: M3 found that no open series splits residents' deposits by currency beyond
one economy (IFS and MFS), so **m1 — local-currency money — can be read only where foreign-currency
deposits are banned, which are closed cells by definition**: an open-against-closed comparison on m1
would have almost no open side. **m1c** (currency alone) is blind to the main road out in open cells —
from local deposits into home foreign-currency deposits — which closed cells do not have, so it would lean
toward refuting with an effect (Q4's twin); **m2** (recorded outflows and net errors and omissions) sees
only what crosses the border. The IMF's Financial Soundness Indicators' foreign-currency share of deposit
takers' liabilities measures liabilities, not residents' deposits. No measure can carry
a verdict. **What part 1 shows instead**: frame k's entries, in cells as they stood at entry and for at
least 12 months before it — **forced** (ka_open at or below 0.25 [0.1; 0.5], or a ban on residents
holding foreign money) and **a substitute at hand** (foreign-currency deposits legal for residents,
foreign cash legal to hold, or a land border with an economy whose legal tender is the dollar or the
euro); **open** = not forced and a substitute at hand, **closed** = the rest; a money whose cell changed
in the 12 months before entry apart — and over **W = 3 years** [2; 5] from entry, side by side, each with
its blind spot said: m1 where readable, m1c, m2, and each also **net of its own change over the W years
before entry** [b-O6]; the open-minus-closed difference within strata of the real return's depth
((−10, −5], (−20, −10], −20 or worse) and π (below 20%, 20–40%, 40% or more), n in every cell. No margin,
no verdict. Money-years under a deposit freeze cannot be read.

**Claim 4 — successors, told** [a-O13; D1]. Frame g cannot be entered by rule (section 5 g), so claim 4 is
**told**: each coin named in sourced reading, less Terra and UST, is mapped onto section 2's
private-issuer lines by two coders apart, κ reported; a mechanism both coders place outside the lines is
said, a split between them is said as a split; no verdict, n given. *A yield is not a support* — decided
from monies before 1900 (interest-bearing notes and exchequer bills circulated on their issuer's credit:
the yield is part of the return; what stands behind it is the payer's solvency, on the account's list).

**Claim 5 — the pattern** [a-O7, a-O8]. Frame c's monies (entrants by c3 and c4 counted from phase 3),
frame d's (from phase 3). *Phases, each reached at its first date*: 1 strain (entry) · 2 debasement (frame
d's cut) or printing beyond the limit — L1, or a C15 episode that is **not accommodation read at its
start** (C12's reading at m0), **reached at the episode's crossing c**, as route c4 enters — an episode
whose c falls on or after the onset is a response, never phase 2 before it [c-O4] (**headline: counted
whatever the regime**; variant: not counted under an
inflation target — the phase-2 rule, fixed once) · 3 two prices (a market split recorded while a parity
stands; where a parallel series is found, the premium at or above **5%** for 3 months, or a year [2; 10],
a variant) · 4 force imposed — **headline: exchange controls imposed or tightened as dated in
Ilzetzki, Reinhart and Rogoff's chronologies** (the source L2 and H1 already read for every money,
1946–2016); bans on foreign money, legal-tender penalties and general price controls are variants, by
source [c-O5] · 5 flight
(m1 — or m1c where m1 cannot be read — fallen **0.20** log points [0.10; 0.30] more since entry than the
median change, over a span of the same length, of all money-years whose **average π over that span**
falls in the same band as the money's own average π from entry to the date (below 20%, 20–40%, 40% or
more) [b-M6]; below the onset nearly every life sits in the lowest band, so the netting does little
there and the pressure strata carry π — said [c-M16]) · 6 broke (frame b's line) · 7 a new money, or
restored. **A phase standing at entry** (a split already recorded, controls in force) is dated at the
entry; in test (i) such phases tie with each other (half-ordered), and a variant leaves them out; in test
(ii) entrants by c3 and c4 enter the risk set at their phase 3 date [c-M4]. A market split first recorded, or
a premium first passing its line, in the month (year) force was imposed is dated *force-made*.
- *Test (i), the order* [b-B1, b-M5]: lives with two or more of phases 2–5 **reached before the life's end
  of reading** — for a life that broke, **its crossing** (phase 6): a phase first reached after the
  crossing is a response to the break, described, **never in C or in its permutations**; for a life that
  **held over H, fully observed**, the whole of H. C is the share of pairs of middle phases in the order
  2 < 3 < 4 < 5, averaged over lives; **two phases first reached in the same year (month) count as half
  an ordered pair**, in C and in the baseline alike. The baseline permutes the phases' dates within each
  life, 10,000 times, **only among the orders the definitions allow** (a force-made market split stays
  after force; no two prices without a parity; convertible and inconvertible lives apart). **Confirmed** if
  C for broken lives is above the baseline's 95th percentile **and** exceeds C for held lives by at least
  0.10 **with the difference's 90% bootstrap interval above 0** (phase 5 is late by construction, which the
  within-life baseline cannot see) [c-O3];
  **refuted** if C for broken lives is within the baseline's central 90%, or does not exceed C for held
  lives; otherwise we cannot conclude. Too thin: fewer than 20 lives **in either group** [a-M8]. *Second
  reading* (the dossier's): lives entering by c1 or c2 only, reported beside; C also **per pair of
  phases** [c-O3]. *Variants*: broken lives read to the onset, said as "phases after the onset may answer
  the fall already under way"; lives with a war year before their end of reading left out [c-M12].
- *Test (ii), the odds* [b-O7, b-M2, b-M3, b-M7]: inconvertible money-years at risk **only before frame
  b's onset** — the years of a counted spell, entry to entry+H−1 [c-M6]; **the event is the onset** (the risk set ends there; the crossing a variant); for each
  middle phase k, the rate of an onset after reaching k against at-risk years that had not, **each
  phase's ratio reported** (the dossier's form), within **the pressure strata** — strain included — in
  **both readings**, the verdict the one both give; a phase first reached in the onset's own year is
  counted apart, its number said; money-years in war years apart, the verdict given outside them and the
  war years' ratios reported; re-entry after restoration; bootstrap over monies. Reported by era; **the
  fiat era is the headline. Margin: 1.5.** Confirmed if phases 2, 4 and 5 each give at least 1.5 with the
  interval above 1; refuted if each of them lies wholly below 1.5; otherwise we cannot conclude. **Phase 3
  is reported, never required** (the market split sits next to the onset's own measures). *Check
  outside*: fitted on the years before 1946, read after — **only for the phases readable then** (phase 2
  has no source before 1950 but frame d's cuts; phase 4 where the chronologies' notes reach before 1946;
  so the check covers phase 5, and phase 4 where readable; with fewer than 20 onsets it is not run, said)
  [b-O7, c-O5]; within the
  fiat era, each World Bank region left out in turn — the scenario (A7) is drawn only if every region left
  out keeps each ratio above 1. Too thin: fewer than 20 onsets in the fiat era.

## 7. The analyses' parameters

- **A2** — frame a as above; nothing fitted; value and trust apart.
- **A3** [a-O11] — the parities fixed before reading: the Bank Restriction at the mint price, £3 17s 10½d
  per ounce of standard gold; the greenbacks at $20.67 per fine ounce. The model: paper's value in gold is
  the discounted chance of resumption at par; before each law a constant hazard λ, P = λ/(λ + r); after it,
  the legislated date T, P = q·e^(−r(T−t)). r is the long government yield (consols; US 6% bonds in gold)
  [the short rate]. **q is read only between 0 and 1**: where the model gives q ≥ 1, or a λ implying
  resumption within a year for three years or more in a row, A3 says for that span that **the premium
  cannot separate an expected return to gold from the paper's own value as money**, and the part's
  outcome "redemption was expected" cannot be read there. Checked on the 1914 suspensions (no calibration
  from them).
- **A7** — the scenario projects the fiat era's rates (claim 5 (ii)) under the Markov assumption, stated;
  no date; the most frequent outcome first; what differs today said of every rate (floating rates,
  inflation targets, interest on reserves, deposit insurance, reserve monies' debt in their own money);
  dropped if claim 5 fails within the class.
- **A9** — frame g **told**: the named coins' phases on their own terms; never pooled into claim 5.
- **A10** — frame f; separators at entry: explicit insurance (Demirgüç-Kunt, Kane and Laeven), the state's
  debt to GDP and its share in its own money (euro members both ways), banks' claims on the state, deposit
  dollarisation; the lender of last resort and solvency not tested. *Statistic*: the difference in the
  share of episodes without a loss, insured against not (and each separator), Mantel–Haenszel over **f1
  and f2 only** × tercile × era × **the state in default at entry or not** — the state behind the account
  goes with having insurance and decides losses [c-O9]; **f3 described, never pooled** [a-O14]. **Margin: 10 points**, decided as
  claim 2 (its twin). While f1 cannot be read (section 5 f), A10 runs on f2 alone, said.
- **A11 — declared (not yet: a B), its rule read from the earliest version that can be had** [c-M14, e-M9]. Jiang, Matvos, Piskorski and Seru's
  version of **5 April 2023** (Stanford GSB Research Paper 4080: "First Version: March 13, 2023 — This
  Version: April 5, 2023"). The first version cannot be had (SSRN serves only its latest revision), and
  every later copy — NBER's revisions of October 2023 and July 2024, SSRN's of April 2024, the *Journal of
  Financial Economics* (2024) — knows the 2023 outflows. The April version's own data are the 2022Q1 Call
  Reports, and banks' 2023Q1 deposits were first published with the Call Reports due 30 April 2023: **its
  rule was fixed before any bank-level 2023Q1 figure** — not before the event: SVB and Signature had failed
  on 10 and 12 March (the narrow check's O5) [e-M5]. *The rule, read from that version only*: a bank is
  *flagged* if it is insolvent in the paper's headline scenario — half of uninsured depositors withdraw,
  assets marked to market as that version marks them [all uninsured withdraw, a variant] [a-M10] —
  **recomputed to 31 December 2022** from frame j's data; the outflow (frame j) regressed on "flagged",
  the uninsured share controlled; SVB, Signature and First Republic out; banks with no 31 March 2023 report
  as frame j [b-M14]. **Margin: 2 points** of starting deposits; confirmed if at least 2 with its interval
  above 0; refuted if wholly below 2. *Its limit, said with the result*: written after SVB failed, it tests
  whether the mechanism named from SVB sorted the **other** banks' outflows — never whether it could have
  foreseen SVB. **Not yet: a B, declared** (section 10) [d-B]. *The six questions* [d-M7]: Q1 every filer,
  by rule — but First Republic is out by name, its run seen by the rule's authors (a variant with it in, if
  A11 is ever run) [d-M8]; Q2 the flag is computed from 31 December 2022 data by a rule published before any
  bank-level outcome — **its recipe is not written** (which items, which prices at which date, whether
  loans are marked, which uninsured field; the frozen FDIC files hold no maturity buckets and no price
  index), and the rule is not shown free of the three banks' runs or the Fed's weekly aggregates [d-O1,
  d-O5]; Q3 the outflow follows the entry **only if** the marking uses prices at or before 31 December
  2022 (the version marks to 2023Q1), and amended filings may put inputs after the outcome [d-O1, d-O2];
  **Q4 — not yet**: the uninsured share is controlled as a straight line, so a run that grows faster than
  linearly in that share loads on "flagged", and nothing holds the deposit path already under way in 2022
  — both can confirm with no effect [d-B]; a refutation leans on total deposits, which include brokered
  deposits bought to replace a run [d-O3]; A11 has no floor and no smallest detectable effect [d-O4];
  its interval, weights, outliers and acquirers' merger jumps are unset [d-M11]; Q5 the flag reads no
  deposit flow, but it reads the 31 December deposit level, the outflow's own base [d-M9]; Q6 that level
  is the outflow's yardstick and the flag's input, with no second yardstick [d-M9]. *Its own disguise*:
  "flagged" is a portrait of SVB — a high uninsured share and a securities book bought with the 2020–21
  inflows; the three banks out remove the portrait's model, not its likeness: a bank can be run for being
  like SVB with no role for insolvency under a run [d-B]. The *JFE* version is cited for the mechanism,
  never read for the rule.
- **A12** — refuges by rule: every asset with a local price at the first public crossing, and those named
  as refuges in sources dated before it; horizons **1, 3 and 5 years** from that crossing, each on the
  breaks that cover it, **and all three on the common set**; deflator: the local price index, never gold;
  the parallel rate where a series is found and the premium is at or above 10%; "protected" = at least
  **80%** of real value kept [50; 90]. Bitcoin: its dollar return and the local fall, apart. **Breaks with
  a recorded market split and no parallel series are flagged and reported apart**: there the official rate
  understates a foreign refuge's local value, so "not protected" could come by measurement [c-O7].
- **A13** — frame h above; its card is M8's.

## 8. The six questions, rule by rule [a-M11, d-M7]

Q1 a case by name · Q2 the outcome or a separator in the entry · Q3 a window at, or an entry after, the
outcome · Q4 every comparator can reach the outcome, and no confirmation without an effect · Q5 a variable
measured by the outcome's own measure · Q6 the questioned value as its own yardstick (BLUEPRINT §8.1 item
11, since 56f1823), answered below the table [d-M7]. The last column asks where the rule's own disguise
would sit.

| Rule | Q1 | Q2 | Q3 | Q4 | Q5 | Its own disguise, and what closes it |
|---|---|---|---|---|---|---|
| The acts list | every money-year of the source | acts are announced decisions; a devaluation within a kept peg is value, a variant | acts dated by their source's year; F1, which cannot be dated, is out of the headline; past a source's last year, *cannot be read* [b-M16] | n/a | L2 dated by announcement, never by a change of de facto class | acts better recorded where monies broke: headline acts from sources coded for every money; the act rate reported by source |
| The regime | by source | lagged 12 months; class 14 never used | — | — | the fine classes put crawls and announced bands with parities, so an announced band dates no market-rate onset; class 9 floating, a variant [b-M1] | carried forward after 2016: flagged, a variant drops it |
| War | by rule | territory or own losses, never participation alone | war inside a horizon coded, not apart | — | — | coalition years with small losses: not war years by (b)'s 1,000 |
| Claim 1 | **told** | — | — | a forward count could confirm with no effect through strain (b-B2); the description says so in words | — | told by step 8: no verdict to disguise; the base rate on the same L-year window as its shares [c-O1] |
| Claim 2 | by rule | inconvertible; separators at entry; "taken back" carries the state's default — **held as a stratum, and the verdict given without it** [c-B1] | H from entry, fully observed; already inflating or past the onset apart, with its variant [c-O6] | pegs and boards must give way before a break: given with and without them; post-2016 regimes with and without | supports by law, not behaviour; a de facto peg stands on value — the without-pegs reading [c-M11] | the count drifting with era: matched by era; fiscal distress inside the count: the default stratum and the without reading (the third audit's repair) |
| Claim 3 | **told** | — | — | m1c is blind to home foreign-currency deposits, open cells' main road: it would refute with an effect — hence told | — | told: every measure beside its blind spot, n in every cell |
| Claim 4 | told | — | — | — | — | told: no verdict to disguise; the coders' split said |
| Claim 5 (i) | by rule | phases from dated acts and measures; phase 4 from the chronologies for every money [c-O5] | **a broken life read to its crossing, a phase after it a response, never in C** [b-B1]; phase 2 by C15 at its crossing c [c-O4]; held over H fully observed | permutations only among allowed orders; ties half-ordered in C and baseline alike; **the margin over held lives with its interval** [c-O3] | flight net of its π band's median over the same span | a force-made split can only follow force: fixed in the permutations; phases after the break making the order: cut at the crossing; a phase late by construction (flight): the held lives' interval |
| Claim 5 (ii) | by rule | at risk only before the onset; phase 2 by C15 at c, a c on or after the onset a response [c-O4] | the event is the onset; competing exits leave the risk set; a phase in the onset's year apart | at-risk years without the phase can break; **strain and default in the strata**, both readings required [b-O7, c-B1]; in practice it cannot refute (said) [c-O8] | the pressure strata; phase 3 never required | phase 2 decided after its start: C12's reading at m0; strain driving both printing and breaks: its route and tercile a stratum |
| Frame a | by rule (four lists) | the change is the entry | window from the change; past the end censored | non-changers can move either way | value and trust apart | belligerents of 1914 in war years: told, neutrals counted |
| Frame b's onset | every break | a second outcome date | every route "stayed" to the crossing, begun within 36 months; none within: at the bound, flagged [b-O2] | n/a | a market split at new controls dates no onset | a chronic premium: the 36-month bound; a slow climb: the bound itself |
| Frame c | by rule | already inflating, or past frame b's onset by any route, apart [c-O6] | one spell per H; c4 at its crossing | convertible apart; pegs as claim 2 | n/a | chained spells: one per H; route ties by order; c4's reclassification lines flagged, a variant drops them [b-O1]; default at entry a matching stratum [c-B1] |
| Frame d | by rule | the cut is the entry | coverage read to entry only | full-bodied coins outside, told | the price index in the unit | a search that finds only famous cases: one procedure on every cut |
| Frame f / A10 | by rule | no rescue or freeze enters | a loss on or before entry, or in an annual entry year: already breaking, with its variant | every account can lose; the state's default at entry a stratum [c-O9] | matched at entry, never to the trough | f3 pooled: described only; insurance going with the state's standing: the default stratum |
| Frame g | told | — | — | — | — | — |
| Frame h | every country-year | published thresholds; percentiles and trend on data to date | hits before the first public crossing; open alarms neither way | false alarms counted | inputs dated at release | a revised series leaking the future: first releases where they exist, the limit said |
| Frame j / A11 | every filer; First Republic out by name [d-M8] | the flag from 31 December 2022 data, by a rule published before any bank-level 2023Q1 figure (after SVB's failure) [c-M14, e-M5]; its recipe not written [d-O1] | one quarter after the entry, only if marked at or before 31 December 2022; amended filings [d-O1, d-O2] | **not yet, declared**: the uninsured share held as a line, the 2022 deposit path not held [d-B]; brokered deposits in the refuting measure [d-O3]; a bank with no Q1 report left out and named, a variant both ways [b-M14] | the flag reads no deposit flow, but the year-end level the outflow is measured from [d-M9] | a portrait of SVB: the three banks out remove its model, not its likeness — declared [d-B] |
| Frame k | by Z | entry by returns, not holdings | entry at the run's last year | — | returns, not flight | feeds claim 3, told |
| A3 | two cases | parities fixed first | — | — | value read as expectation | a model with no money value in paper: q only in [0, 1], else "cannot separate" |
| A12 | by rule | refuges named before the crossing | horizons from the first public crossing; the common set | — | the local price index | foreign refuges at the official rate where controls bind: flagged, apart [c-O7] |
| Case-line check | — | — | an annual measure for a monthly entry refused; apart lines exempt, never counted [b-M12]; a counted line whose onset is not after its entry refused [c-O6] | — | — | a list coded before its rules or its acts: the commit-order check, the order declared in the twin [b-M13, c-M2] |

**Q6, the questioned value as its own yardstick** [d-M7]. Where a rule reads a money's value on a measure
the support under test can set, the grid asks for a second yardstick, and a sign only where both agree.
v4.1 fixes no new rule: the table names what each rule already reads beside its yardstick, and where that
is not a second yardstick in the grid's sense, the hole is declared (section 10):

| Rule | Its yardstick | Can the questioned support set it? | The second yardstick |
|---|---|---|---|
| The acts list, war, frame c's entry, A3, the case-line check | acts, dates, pressure measures; gold for A3 | no: none reads the money's value on its own terms | — |
| The regime | Ilzetzki, Reinhart and Rogoff's classes | the official rate, under controls | none stated in M0: declared [e-M3] |
| Frame b's onset and crossing; claim 2's "broke"; claim 5's phase 6 and the order before it; frame h's hits (frame b's crossings) | π, and the official rate under a parity | **yes, under force**: price controls hold π, exchange controls the official rate | **none for "broke"**, read on π alone: the depreciation route dates the onset, not the break, and the recorded market split is phase 3 and a stratum, not a reading of "broke"; the premium only where a series is found by hand — **for force, declared** [e-M3] |
| Frame a | value (π, depreciation, the market split) and trust, apart | the change under test can bring controls | value already read on three measures side by side, counted-free |
| Frame d | the price index in the unit | no: a debasing mint does not set Allen and Unger's market prices | the metal content is the entry, the prices the outcome |
| Frame f / A10 | a loss on the account, in its own money | a nominal account hides a loss by inflation | declared: A10 reads cuts and access only; a loss by inflation is claim 2's and part 2's |
| Frame j / A11 | the 31 December 2022 deposit level | the flag reads it too | declared [d-M9] |
| A12 | the local price index, as deflator | **yes, where controls hold it**: a refuge looks protected | the breaks with a market split and no parallel series already apart [c-O7]; beyond them, none: declared |
| Claims 1, 3 and 4, A9, frames g and k | told | — | claim 3's m1, m1c and m2 side by side |

## 9. What M0 changes in the dossier and the maps

To be written into the dossier (sections 3, 5, 8, 11 part 1 pages 5–7 and part 3 page 6, 13, 14), the map
of the whole, the part 1, 3, 4 and 5 maps and the guards table — each departure in the map's change log:

1. **Claim 1 is told, not counted** (`ft-map` step 8, after five rounds found the same kind of hole): each
   break's dated line, the shares of onsets after, before and in the year of an act beside the base rate
   of acts on the same window, and the forward table as a description with its limit said. **Part 1's
   timing is described, never counted**; claim 5 counts the order of phases and the odds after each. The
   dossier's backward count against matched controls, and v2's forward test with its margin, are gone.
2. **The acts** — a devaluation within a kept peg is value, not an act; L2 counts a regime abandoned by an
   announced decision; F1 is a variant only (it cannot be dated); past a source's last year an act
   *cannot be read*, never "none".
3. **Claim 3 is told, not counted**: open against closed cells, m1 where readable, m1c and m2 side by
   side with their blind spots, within depth and inflation strata, n in every cell — no open series splits
   residents' deposits by currency. The "stay" bars, "mixed" and constant-rate dollarisation are dropped;
   **the substitute now includes a land border with a dollar or euro economy** [b-M8].
4. **Claim 2's count** — among *taken back*, *a limit by rule*, *a limit by institution*, *force* (the
   limit split in two, since frame a's reforms change the institution); given with and without pegs and
   boards; from 1970; spells, *broke and restored* not held; **the state in default at entry a matching
   stratum, and the verdict given without "taken back"** (its condition is not being in default) [c-B1].
5. **Claim 4 and A9 are told**, and frame g is not entered by rule: DefiLlama's terms bar commercial copying
   (D1), and no open census includes dead coins.
6. **Claim 5 (i)** reads a broken life only to its crossing; ties half-ordered; the debt-and-deficit
   reading beside. **Claim 5 (ii)** at risk only before the onset, the onset its event, per phase, within
   the pressure strata with strain, in two readings; flight net of its inflation band; phase 3 reported,
   never required; c3 and c4 entrants from phase 3; the check before 1946 on the phases readable then.
   **Phase 2 by C15 is reached at the episode's crossing**; **phase 4 is read from Ilzetzki, Reinhart and
   Rogoff's chronologies** for every money (other kinds of force by source); test (i)'s margin over held
   lives carries its interval [c-O3, c-O4, c-O5].
7. **The onset**: every route "stayed" to the crossing and began within 36 months, or at the bound; the
   depreciation route on the official rate under a parity; the premium route a variant (no open
   parallel-rate series). "Two prices" in the headline is a recorded market split.
8. **War**: by territory or own losses; a case entering in a war year is apart; war inside a horizon coded.
9. **Frame f**: f1 is an annual return (Baron, Verner and Xiong's own definition; the dossier said
   "cumulative"); matched on the crossing year's return, not the months it took; the entry-year rule on f1
   too; f3 never pooled into A10; f1 cannot be read until Baron, Verner and Xiong's data can be fetched.
   **A10's headline is insured against not** (the dossier asked about "more supports standing"), with the
   state's default at entry a stratum, in frame f's matching too [c-O9, d-M5].
10. **Sources**: the Global Macro Database is not used (D1); Mauro et al.'s FPP is not in the order (the
    IMF's site refuses the toolkit); debt from the HPDD mirror then the WEO; deficits from the WEO and
    Jordà–Schularick–Taylor; Ilzetzki–Reinhart–Rogoff to 2016, carried forward after; frame c's route c4
    reads the pilot's **C15**, its declared holes with it.
11. **A3**: q only in [0, 1], else "the premium cannot separate".
12. **A11's rule is read from the version of 5 April 2023**, the earliest that can be had (the first
    version cannot be; every later copy knows the outcome); *flagged* fixed; the limit said (written after
    SVB); banks with no Q1 2023 report named [c-M14]; **the narrow check's B declared, and A11 waits on
    Sami: declared or told** (section 10) [d-B, e-M9]. **The dossier's "(their own robustness case)"** for
    31 December 2022 is dropped: D1's description of the version does not confirm it (the narrow check's
    M10) [e-O5].
13. **Hammond (2012)**: the targeters at the start of **2012**, not 2010 (D1's reading of the handbook).
14. **The pound in 1975** enters frame b by the headline line; **frame c's 90% line** reported apart outside
    its fitting sample; **A13's card** is M8's [b-M8].
15. **Frame a's Garriga panel and act L3 read Garriga's own reform coding**; L1 reads her lending-limits
    component; a change of the index of 0.05 is a variant [c-M3, c-O10]. **A12** flags and sets apart the
    breaks with a market split and no parallel series (the dossier's "at the parallel rate where the official
    one was controlled") [c-O7]. **Frame c** sets apart an entry past frame b's onset by any route [c-O6].
16. Every parameter the dossier left to M0 now has a value and a grid (the twin YAML).

## 10. What is left to the missions, and what is told

- **Data** (M2–M9): where a headline source is behind a wall, the mission waits and the wall is declared
  (E2's Engine notes); no source is swapped to get round it. AREAER's text is for Sami's list.
- **Told by design**: claims 1 and 3 (section 6), claim 4, A9, frame g. **Told, not counted, if the data
  do not reach the floors**: claims 2 and 5 and A10, each said, with n in every cell; A11 has no floor —
  declared below [e-O3].
- **Round 3's B1, declared** (`ft-map` step 8, the third round with a B): claim 2's count carried the state's
  default, fiscal distress its matching did not hold. The repair written here — default at entry a
  stratum, the verdict given without "taken back" — is the auditor's, simulated there at 0–3% false
  confirmations; it was not put through a fourth round of design. The narrow check of v4 finds the two
  repairs done as round 3 simulated them, at 0–1% false confirmations together [d-Q1]. **Put to Sami** in
  the session's summary.
- **A11's B, declared** (the narrow check of v4) [d-B]: "flagged" can confirm with no effect of insolvency
  risk — through the uninsured share, held only as a line while a run grows faster than linearly in it
  (up to 45–100% false confirmations in the check's null, where the flag rises with that share), and
  through the deposit path already under way in 2022, which nothing holds (up to 21–66% in the check's
  worst cells, whichever way the flag goes) [e-M2]. **What a reader must be told if A11 is run as written**: a "confirmed" shows that banks like SVB
  lost more deposits in early 2023, not that insolvency under a run sorted them; a "refuted" leans on total
  deposits, which include brokered deposits bought to replace a run. Open with it [d-O1–O5, d-M8,
  d-M9, d-M11, e-O5]: the flag's recipe is not written, and the frozen FDIC files hold neither its maturity
  fields (offered by FDIC's API, not asked for) nor any price series; amended filings may carry the outcome
  into the flag; no floor, no smallest detectable effect; its interval, weights, outliers and acquirers'
  merger jumps unset; whether the rule changed between 13 March and 5 April 2023 cannot be checked; First
  Republic is out by name (a variant with it in); the 31 December deposit level is both the flag's input
  and the outflow's base, with no second yardstick. **Put to Sami** (step 8): A11 stays declared, or is
  told as v3 did — the session recommends told (`plan/e2-ft001.md`, Decisions, "M0 v4's narrow check").
  **"Declared" cannot run as written**: it means a new version of these rules writes the flag's recipe
  (and its floor) before any bank is read, and the lock holds every list to that version [e-O2]. **Until he answers, no bank is read for A11 and no A11 verdict is computed.** For the
  record, not a rule: in the check's null cells, the uninsured share held finely and each bank's own 2022
  path bring false confirmations to 0–2% — a repair that would be a fifth round of design, on Sami's word
  only.
- **Frame d waits** on Karaman et al.'s series (a wall and a purchase, section 5 d).
- **Declared, not closed**: in claim 5 (ii), acts or phases answering inflation expected but not yet in
  any price or rate, and strain beyond its route and tercile; frame d's pattern has no check outside A7's
  fitting sample; the market split is a yes or no where a premium's level would be finer; C15's
  reclassification lines and December spikes (the pilot's O1 and O2); **test (ii) cannot refute in
  practice** (section 6) [c-O8]; A11's recomputation reads FDIC's current database, not first filings;
  in claim 2, strain beyond what its matching holds (route, tercile, era, the state's default), as in
  claim 5 (ii) [d-M3]; where force holds the price index or the official rate, a money's "held" (claim 2),
  its crossing and the order before it (frame b, claim 5) and a refuge's protection (A12) are read on
  yardsticks the force sets, no second yardstick open — the recorded market split is a phase and a stratum, not a reading of "broke"
  (section 8, Q6) [d-M7, e-M3]; the regime's classes carry no second yardstick M0 names [e-M3]; A10 reads a
  loss on the account in its own money, so a loss by inflation is claim 2's and part 2's, not A10's
  (section 8, Q6) [e-O5]; an L1 act can leave the statutory cap standing — a fall of `cuk_limlen` that
  stays at or above 0.5 [d-M6].
