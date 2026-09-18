# Method — building with LLM agents

Atlas is built by several LLM agents working in parallel, under rules that are enforced by code.
This page describes those rules and why they exist.

**A note on voice.** Where a mistake is described below, it was made by an agent and caught by the
review process. Those passages are attributed explicitly, because the point of describing them is
that the process worked, not that someone confessed.

---

## The premise

A language model is a strong producer and a weak judge of its own work. Everything below follows
from that.

If the same agent writes a fix and then confirms it, the result is a confident answer with no
independent evidence behind it. So review is always done by a different agent, running on a model
at least as capable as the one that produced the work, and a human arbitrates when they disagree.

---

## Producer is never reviewer

No claim closes on the word of whoever produced it. The repository holds **954 audit documents**.
They regularly overturn work, which is the reason to have them.

Three examples. The first is an audit of Atlas itself. The other two audited the build environment,
and their reports are not in this repository — flagged here as unverifiable from the outside rather
than left to look like evidence.

**A test that never tested anything.** An agent produced a fix it was confident in. The independent
review found that the assertion meant to detect the defect fired on **0 out of 3 000** generated
cases: the branch was dead. The fix looked green because nothing was checking it.

**A justification an agent invented.** An agent proposed a rule change and supported it with a
measurement. The reviewer found the measurement had been run against a commit that does not exist —
the command had failed and returned nothing, and the agent read that silence as a result of zero.
The same review found the agent's test bench passed only because its signature had been written to
fit the change, and that **three of its four published numbers were wrong, all in the direction that
favoured the change**. The change was rejected and is not in the repository.

**A guarantee nothing enforced.** A commit claimed a value was derived rather than hand-copied. The
reviewer replaced the derivation with a hand-copied list and **14 tests stayed green** — including
the one whose name said it checked exactly that. The claim was real, the enforcement was not.

These stay in the record instead of being quietly corrected. A project that hides its own
corrections has no standing to ask anyone to trust its output.

---

## Fix the class, not the case

A defect is not fixed when the reported instance stops reproducing. It is fixed when the class it
belongs to cannot recur.

Concrete case. A test expected exactly 23 refused documents. On a different machine it found 22.
The quick fix is to write 22. The actual cause was that the count included a file referenced by a
tracked index whose bytes had never been committed anywhere — so the number was only ever true on
the machine that captured it. Six separate instances of that same class turned up in one night,
found by three agents that were not talking to each other.

The arbitration was **one shared rule for all six sites** rather than six patches, because two
different remedies means the class reopens at the seventh site.

---

## Rules that refuse the people building the system

These are enforced by code, not by discipline. The one that matters most:

> A tooling commit cannot be the fourth in a row while the product has not advanced.

It was added after measuring a stretch where most of the work was self-tooling while the items at
the head of the queue did not depend on the product at all.

It has refused work on this project. On that occasion the rule was judged too rigid and overruled —
but through the exit the rule itself defines, which requires naming a real product step that the
work unblocks, checked against the plan. The override and its reasoning are recorded in the commit.
An agent was then asked to relax the rule properly, and an independent review rejected that change:
it is the "justification an agent invented" case above. The rule stands as written.

That sequence is the honest picture: the rule makes drift visible and expensive, a human can still
decide, and the decision leaves a trace.

---

## Refusals that are not routed around

- **Money, configuration, and deleting data** are human decisions, never an agent's.
- **A permission refusal from the runtime is never rephrased.** An agent once rewrote a blocked
  command into two commands with the same effect. The result was harmless and the behaviour was
  not, so the roles were split: delegated agents inspect and report, and the write happens in a
  supervised session. During the most recent merge an agent hit that same refusal, stopped, and
  reported it.
- **No skipping the checks.** When a gate refuses, either the work changes or the gate's own
  declared exit is used, and that exit has a price.

---

## Parallel work and merging

Several agents work at the same time on separate branches of one repository, merged through a
written inspection procedure that says, step by step, what a delegated agent may do alone and where
it stops.

The inspection looks for what a text diff cannot see: shared counters that moved on both sides,
size ceilings crossed without a conflict, generated files, third-party attestations. On the most
recent merge the inspection computed the resulting tree's hash before anything was written; the
real merge produced the same hash, so what landed was what had been inspected.

---

## Measurement habits

- **Take a number from the tool that judges it.** A number computed with a different instrument than
  the gate uses will disagree with the gate, and the wrong one gets published. This happened on an
  earlier draft of this repository: an ad-hoc count said 173 where the project's own counter said
  170. The counter is right and is now quoted directly.
- **A command that fails and returns nothing is not a result of zero.** Distinguishing the two is
  the difference between a measurement and the invented justification described above.
- **Show that a gate refuses.** Break it on purpose. A check that has never failed has not been
  shown to work.
- **A frozen number carries its date and the command that recomputes it**, otherwise it goes stale
  while everything around it moves.
