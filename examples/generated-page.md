# A real generated page

This is the actual output of the report engine, copied unchanged from the private repository. It is
short, and that is honest: the store holds 7 records today. The chain works; the corpus is not
built.

The engine writes in French. The English walkthrough follows.

---

## The output, unchanged

> # Le rapport du jour
>
> *Produit par `engine/rapport/rapport_du_jour.py` depuis
> `state/mesures/lignes/lignes-ancrees.jsonl`, dans un processus qui n'a jamais eu ces lignes en
> memoire.*
>
> **Selection : 1 ligne(s) retenue(s) sur 7 au magasin**, par coordonnees `reference_period` =
> `2024`.
>
> - **GDP (current US$)** — USA, 2024 : `29298013000000` *(serie `NY.GDP.MKTP.CD`, ligne
>   `rejeu-positif-worldbank-gdp-usa|NY.GDP.MKTP.CD|USA|2024`)*
>
> ## Ce que cette page n'affirme pas
>
> Elle ne dit pas que ces observations sont les BONNES, ni que la selection est complete au sens du
> contrat : elle est **ECRITE A LA MAIN**, sous l'autorisation de `A09-1` qui reste ouvert. Le jour
> ou cet item ferme, ce producteur REFUSE de tourner tant que la selection n'est pas derivee de
> l'objet de contrat qu'il aura produit.
>
> Elle ne porte **aucune notion d'echelle** : cet axe n'a aucun porteur dans le magasin ni dans le
> contrat. Le « triplet » n'a donc que **deux** coordonnees portees sur trois.

---

## What it says, in English

**The header states its own provenance.** The page was produced by `rapport_du_jour.py` from the
anchored store, *in a process that never held those records in memory*. The renderer is a separate
process from the producer. That is not a performance choice: it means the page cannot contain
anything that was not read back from disk.

**The selection is stated with its denominator.** "1 record kept out of 7 in the store", and the
coordinate used to select (`reference_period = 2024`). A page that showed one number without saying
how many it chose from would hide the size of what it ignored.

**The single line carries its identifiers.** The series code `NY.GDP.MKTP.CD` and the record id,
which is the same id you can re-check with
[`verify_anchor.py`](verify_anchor.py) in this folder.

**Then a section titled "what this page does not claim"**, which the engine writes itself:

- *It does not claim these observations are the right ones, nor that the selection is complete.*
  The selection is **hand-written** at this stage, under an explicit authorisation from plan item
  `A09-1`, which is still open. When that item closes, the producer **refuses to run** until the
  selection is derived from the contract object rather than chosen by a human.
- *It carries no notion of scale.* That axis has no carrier in the store or in the contract, so the
  intended three-coordinate addressing currently resolves on two.

---

## Why this page is in the repository

Because the interesting property is not the number. It is that the page names what it cannot
support, and that a plan item is scheduled to take away its permission to run in the current shape.
A component that will refuse itself later is a design decision, and this is what it looks like
before the deadline arrives.
