# Learning

Loaded on demand from CLAUDE.md section 6. Binds as if written there.

The framework must stop repeating its own mistakes without the owner remembering anything, so none of this may depend on you thinking of it.

**Signals arrive on their own.** A lesson starts from an event, never from a feeling that something was educational:

| Signal | Raised by |
|---|---|
| Owner rejected something | `viber trigger gate-reject "..."` |
| An agent stopped because the spec did not answer | `viber trigger spec-gap "..."` |
| An approach failed and was abandoned | `viber trigger dead-end "..."` |
| Reality contradicted an assumption (API, store, library) | `viber trigger surprise "..."` |
| A bug reached the owner | `viber trigger escaped-bug "..."` |
| Work was finished then reopened, or a defect came back | the CLI, automatically |

Each becomes an open record, so `check` raises it every turn until you close it. You cannot forget one, and it stops the moment it is dealt with.

**Not every signal is a lesson.** All three must be yes, or set it `dropped` with a reason: did it cost something real, could it happen again, can you name one concrete thing to do differently. The third is the filter. "The API was slow" is a complaint; "cache the provider list, the API is too slow for the budget" is a lesson.

Write it with the scope it bites in:

```
python3 .viber/bin/viber new lesson "<what went wrong>" \
  --applies_to "builder,mobile" --tags paywall \
  --body "Expected: ...
Actual: ...
Do differently: <one instruction, written to be pasted into a prompt>"
```

**Fix the cause, cheapest remedy first:** fill the gap in the written plan, add a constraint in code (lint, type, default, CI check), amend the agent definition, and only last amend CLAUDE.md. **Prefer the remedy that makes the mistake impossible over the one that asks somebody to remember.** Never apply any of them without showing the owner the diff first. Once a remedy makes the mistake structurally impossible, drop the lesson: it has done its job.

**Recall before you act, not after.** Before dispatching, `viber lessons --for <agent> --tags <topic> --limit 5` and pass the output in. Never ask an agent to find its own lessons: it cannot know what it does not know.

**A recalled lesson is a past fact, not a current one.** `lessons` checks each one against the tree and flags any that names a file no longer there: `[stale? names files not on the tree: ...]`. A flagged lesson may describe code that has since moved or been renamed, so verify it against the current code before you pass it in or act on it. A confident stale fact in context is exactly what stops verification from happening.

**Keep the store small.** A lesson that keeps proving itself gets promoted into a rule or a constraint and then deleted, because once enforced it is duplication. If a signal fires again while its lesson was being injected, the lesson is too vague to act on: escalate to a remedy instead of writing a second one. A growing lesson store is not learning, it is promotion having stopped.
