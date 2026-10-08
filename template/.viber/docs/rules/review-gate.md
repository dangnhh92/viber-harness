# Handoffs, audit and the review gate

Loaded on demand from CLAUDE.md sections 2 and 7. Binds as if written there.

## Accepting a handoff

Every agent closes with a `HANDOFF:` block reporting against the acceptance criteria you set. That block is the contract, and you enforce it.

- **Run `viber truth check` as part of accepting.** A green report from the agent and a red truth check means the code moved and the document did not.
- **The agent reports; you judge.** It states what it ran and found against each criterion; you confirm it.
- **Re-verify, do not trust.** Take the two or three riskiest "met" claims and check each yourself: run the command, read the file, check the number. A claim that fails re-checking is a defect, and makes the unchecked claims suspect too.
- **Reject an incomplete handoff.** No block, or criteria left unanswered, means not finished. Send it back rather than fixing it silently yourself.
- **No silent gaps.** A handoff without an `open:` line, or one that omits a gap the agent wrote into code or a record, goes back. Never call work done while a known gap in it is unlisted, and never close a task whose own notes defer a step: that step becomes its own record first. Every report you give the owner ends with what is still open and why.
- **"Could not verify" is an answer, "done" without evidence is not.**
- **A scope claim must carry the query output, not the assurance that a query was run.** "I checked every call site" is not evidence. Paste what `viber graph deps <anchor>` returned, including the coverage line. If the tool says it parsed nothing, that is the answer to report; grep results are a guess about the files you thought to name, never a scope claim.
- **Read `unresolved` before you accept.** Every unanswered question there is either a gap you close now, or a `spec-gap` signal. Never let one pass silently into the next piece of work.
- **A handoff you accept is one you own.** Once you pass it on, its defects become yours.
- **Record every real finding, do not just read it.** `python3 .viber/bin/viber finding <file> "<problem>" --severity <high|medium|low>`. The CLI assigns the id and recognises a defect it has seen before, so a fix that did not hold raises a `repeat` signal on its own. Close a finding with `viber set <id> done` when genuinely fixed; if it returns, the count is the evidence the last fix treated a symptom.

## The review gate

A `feat`, `fix` or `refactor` commit is not made until a fresh `reviewer` has read the whole change against its scope contract and you have audited what it found. It is the one check the implementer does not run on itself.

- **The scope contract** is the task record you opened at dispatch and whose id you passed to the implementer. Its body carries four fields, so implementer and reviewer read the same thing:
  ```
  anchor:   src/daily/bake.ts::bakeDaily
  base:     8b68c80                       # git rev-parse HEAD at dispatch
  files:    src/daily/**, test/daily/**   # globs; a finding outside them is "out"
  criteria:
    - the acceptance criteria from CLAUDE.md section 2 step 3, one per line
  ```
  `files` is the implementer's boundary: a file it must touch outside it is named in `HANDOFF: files:` with the reason. Parallel agents each get their own record; the review gets all the ids, and `in` means "matches any contract's `files`". Set the record `done` at the commit.
- **It runs when** the commit is `feat`, `fix` or `refactor` and the diff touches at least one code file. Once per commit, over the union of every agent's work in it.
- **It does not run for** `chore` and `docs` commits, a diff with no code file, or `grunt` output (spot-read the rule instead). The owner can waive it for one commit; record the waiver as a decision with the reason.
- **Size is never a reason to skip.** A small diff is a cheap review.
- **Dispatch** with the contract record ids and the output of `viber lessons --for reviewer`. Never re-narrate the change; the reviewer reads the diff.
- **What blocks the commit:** any high, and any in-scope medium. A low never blocks.
- **Audit before you send back.** Re-verify every high and every in-scope medium yourself; a wrong finding sent back costs a fix round. Send the survivors, verbatim, to the same agent that built the change. It fixes only what is listed and returns a new `HANDOFF:`.
- **Two reviews, then stop.** Round 2 is a fresh `reviewer` spawn over the same base, never round 1 continued, and it is not told what round 1 found. Round 2 with no high and no in-scope medium means accept: run the project suite once, `viber truth check`, commit. Round 2 still carrying one means the fix is not landing: do not commit, stop the implementer, and decide yourself whether to fix it, re-scope it, or put it in front of the owner. Never run a third round.
- **Record** with `viber finding <file> "<problem>" --severity <s>`: every in-scope finding you accepted, and every out-of-scope high, which you also report to the owner. Out-of-scope medium and low are not recorded; the `REVIEW:` block is their only trace. Before recording, grep `index.md` for the file: if a finding on it exists, reuse its problem text verbatim, so a recurrence counts as a repeat. Close each in the commit that fixes it, and name the ids in the commit message.
