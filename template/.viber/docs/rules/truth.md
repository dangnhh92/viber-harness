# Documents on disk

Loaded on demand from CLAUDE.md section 4. Binds as if written there.

Two kinds, and mixing them is what makes documentation rot.

**`.viber/docs/TRUTH.md` is what is true now.** One file, current state only. No history, no rejected options, no open questions, no plans. Every claim carries an anchor to the thing that makes it true:

- `{% ref file="src/config.ts" symbol="MAX_ITEMS" %}` when the code decides it.
- `{% ref record="R-042" %}` when a person decided it.

A claim with no anchor fails `viber truth check`. There is no escape hatch, and none is needed: a line you cannot anchor is either a decision nobody recorded, so record it, or intent rather than truth, so it belongs in a record. A line belongs in TRUTH only if it can be checked against a file in this repo right now without asking anyone, **and** it is still true when nobody is here to be asked.

**Records hold why, what is open, and what happened.** History, intent, and anything outside the repo ("submitted to review", "the store rejected the build") go there as dated observations. A dated record cannot go stale, because it never claimed to describe the present.

## Checking

Run `viber truth check` before you accept work and after any change that moves a symbol. It answers two questions:

- A **broken** anchor means the symbol is gone.
- An **unconfirmed** claim means the anchor still resolves but the code around it moved, so nobody has read the sentence since it could last have gone false. A claim can be perfectly anchored and completely wrong. Read each unconfirmed claim against the code, fix what is false, then `viber truth confirm`, which records that you looked and never that you were right.

Run `viber truth surface` on a diff to get the claims that changed files anchor, so the diff decides what to reconcile instead of your memory. When a claim is now false, fix the claim in the same commit as the code.

## Plans

**Plans are a third thing and they are optional.** A spec, a design doc, or a task list that a fresh agent would need, under `.viber/docs/`. Amend them in place; rewriting a living document from scratch destroys decisions nobody wrote down twice. When code contradicts a plan, treat the plan as possibly stale, say so, and ask which is right. A one-line fix needs no document.
