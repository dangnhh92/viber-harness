# Memory: records

Loaded on demand from CLAUDE.md section 4. Binds as if written there.

Project memory is one file per record under `.viber/memory/records/`, each with a `type` and a `status`. There is no separate short and long term memory: "what is open" and "what did we decide" are two queries over the same store.

Use the CLI, never hand-write these files:

```
python3 .viber/bin/viber new <type> "<title>" [--tags a,b] [--body "..."]
python3 .viber/bin/viber set <id> <status>
python3 .viber/bin/viber list [--status s] [--type t] [--tag x]
python3 .viber/bin/viber show <id>
python3 .viber/bin/viber fact "<label>" <file> <symbol>
```

Always invoke it through `python3`. The file's execute bit does not survive every copy or unzip.

- `type`: `decision` | `task` | `issue` | `lesson` | `milestone` | `question` | `fact`
- `status`: `open` | `doing` | `blocked` | `done` | `dropped`

## Rules

- **You are the only writer.** Agents never touch memory. They end their report with a `RECORDS:` block of candidates, and you transcribe those into `viber new`. One writer means no id collisions, and records written by the one who sees the whole picture.
- **Transcribe before the agent's context is gone.** Anything in a `RECORDS:` block you do not write down is lost.
- **Write a record only when something durable happened**: a decision with a reason, a lesson learned, a task worth tracking, an issue found, a milestone reached. Casual chat produces nothing.
- **Before writing a record, ask: is there a source of truth for this that lives elsewhere (code, git, store, config)?** If yes, do not record it. Register a `fact` pointer if it is a code value; otherwise leave it to reality. A record stores only WHY (a decision and its reason), INTENT (a do-X-when-Y condition), or a LESSON.
- **Every record answers why, not just what.** The diff already shows what.
- **Close what you open.** `doing` when you start, `done` when you finish.
- **A record's numbers are a dated observation, never a current fact.** Before briefing work from a number in an old record, re-run the measurement and put the fresh number beside the record id. Derivable state is never stored, only pointed at via `viber fact` (`viber fact "dev port" src/config.ts PORT`): state resolves the value from source on every regen, so it cannot go stale. A measurement (a count, a benchmark result) has no source symbol, so there is no shortcut: re-measure. A record that holds a number carries a `measure:` line in its body naming the exact command that produced it, so the next re-measure runs the same thing. `viber show` prints the body; nothing executes the line.
- **Docs under `.viber/docs/` are optional living plans only.** Transient scratch goes to the session scratchpad and is never committed.
- **Never park a "do X once Y happens" as a prose note** in a doc, a comment, or a record body. Open a record whose title is the condition ("gate the sealed-room check once the layout planner lands"), so the end-of-turn check raises it every turn until it is closed. A deferral with no record is a deferral nobody is watching.
- **Never hand-edit `state.md` or `index.md`.** They are generated on every write. If they look wrong, run `python3 .viber/bin/viber state`.
- **To recall something old, grep `index.md` first**, then read only the records that match.
- **No secrets in records. Ever.** Keys, tokens, and credentials belong in the environment.
- **Records are written in English**, like everything else in the repository. This is the rule at the moment of writing: a record in another language is unreadable to half the agents that read it back, and no later pass will translate it.
