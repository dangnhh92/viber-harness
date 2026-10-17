---
name: harness-audit
description: Use when the owner asks whether the harness (viber, hooks, agents, any orchestration around them) is running properly and accurately, where it wastes tokens or work, or where it has holes; also for "check what is running on this machine". A method to follow, not a tool to run.
---

# Harness audit

Judge the harness by what actually happened, against its own rules. The audit reads; it never fixes. Each finding goes to the owner with a proposed change, and nothing changes until they approve it. Never build an automatic improvement loop.

## Ground rules

- **Evidence for every finding**: session id and timestamp, commit hash, record id, or file and line. No evidence, no finding.
- **Count before you judge.** Turn "the harness sometimes forgets X" into "X happened 3 of 41 times since <date>".
- **Read narrowly.** Transcripts run to gigabytes. Never cat or Read one. Use `tokens.py` (next to this file), or write a small stdlib script in the scratchpad that streams the JSONL and prints counts, sizes and ids, never message text. When the reading spans many projects, hand it to an `analyst` with this skill named in the brief.
- **Respect secrets**: never print `.env` files, keys, credentials, or any file a project marks secret, even when a transcript path points at one.
- **Kill nothing, restart nothing.** List processes; only the owner's decision removes one.

## Data sources

| Source | Where | What it tells |
|---|---|---|
| Session transcripts | `~/.claude/projects/<encoded project path>/<session>.jsonl`, subagents in `<session>/subagents/agent-*.jsonl` | every tool call, its input and result size, usage per call, who started each turn |
| Hook results | transcript lines `type: attachment` with `attachment.type` `hook_success`, `hook_additional_context` or `hook_cancelled`, carrying `hookName`, `exitCode`, `durationMs`, `command`, `stdout` | whether each hook fired, failed or ran slow, and what it injected |
| Compactions | transcript `type: system`, `subtype: compact_boundary`, with `preTokens` and `postTokens` | context size at each compaction |
| Summary sources | `python3 .viber/bin/viber compactions [--last N]` | per summary, how many lines with a number name a path, command or agent id |
| Token report | `python3 .claude/skills/harness-audit/tokens.py --since <date> [--project x] [--session id] [--json]`, run from the project root | cost per project and session, main against subagents, what starts each turn, re-reads, large tool results, cache rebuilds, compactions |
| Spawn log | `.viber/memory/.spawns.jsonl` (`agent`, `model`, `effort`, `refused`) | the agent, model and effort of each spawn |
| Records | `.viber/memory/index.md`, the records dir, `viber doctor`, `viber check` | open signals, findings and repeats, stale titles, decisions |
| Git | `git log` per project, `git log origin/<branch>..` | commits by type, review gate, unpushed work |
| Other orchestration | any relay, scheduler or bot log the project keeps (find it in CLAUDE.md or the repo) | delegated runs, their cost and outcome |
| Machine | `ps`, `lsof -iTCP -sTCP:LISTEN`, `launchctl list` and `~/Library/LaunchAgents` (macOS) or `systemctl --user` (Linux), `crontab -l`, `df -h` | what is running and who started it |

Claude Code deletes transcripts older than `cleanupPeriodDays` (default 30) in `~/.claude/settings.json`. An audit that must look back further needs that raised first; say so when the window is cut short.

## The checks

Run the sections the question needs. For "is everything ok", run all five.

**1. Is it running?**
- Every hook in `.claude/settings.json` shows up in transcripts since that file last changed. Look for a non-zero `exitCode`, `hook_cancelled`, and `durationMs` over 2000 (a slow hook taxes every prompt).
- `viber doctor` in each active project: dead hooks, agents without `model:`, a viber binary behind the release it was installed from.
- After each `compact_boundary`, the recompact hook fired, and the guard injected each on-demand rules file at its trigger.
- Each finished agent left a file in `.viber/handoffs/`, and the recompact output named the newest.

**2. Did the work follow the rules?**
- Every `feat`, `fix` or `refactor` commit that touches code has a `reviewer` spawn before it in that project's transcripts (`.viber/docs/rules/review-gate.md`).
- Spawns: none is `general-purpose` or bare; every one names a model and an effort; none runs at `low`. Check a sample against the routing table in CLAUDE.md, for example `builder` on a decided brief, or `haiku` on a read over 100k tokens.
- Handoffs: each agent result has a `HANDOFF:` block, and the orchestrator ran at least one verifying command after it before reporting to the owner.
- Every `RECORDS:` block in an agent result was transcribed: a matching `viber new` follows it.
- Any project-specific delegation rule in CLAUDE.md, checked against its own log.

**3. Was it accurate?**
- Owner corrections: find owner messages that reject or correct the work, in whatever language they write (insults, "that is wrong", "I already did that", "nobody asked for this", "waste of tokens"). For each, name what the harness got wrong and whether a memory, lesson or rule now covers it. When a correction repeats after a rule exists, that rule does not work.
- Repeats: `viber finding` repeats and reopened records.
- Stale truth: open records whose title contradicts a later done record or the code, and reports to the owner that quoted a record without re-checking it.
- Claims checked later: an agent's "met" that turned out false.

**4. Where is the waste?**
- From `tokens.py`: the share per project, main against subagents, notification wakes, re-reads without an edit, the largest tool results, mid-session cache rebuilds.
- Agents or delegated runs killed, re-dispatched or superseded (a stop, the same task sent twice).
- Work the owner did not ask for: dispatches a later owner message cancelled or called unneeded.
- Model or effort above need: `opus` or `high` on decided work that someone re-checks anyway.

**5. Where are the holes?**
- Rules with no enforcement: a CLAUDE.md or rules-file rule that no hook checks, and that checks 2 and 3 show being broken.
- Deferrals parked as prose instead of a condition record.
- Processes, ports, scheduled jobs and lock files with no owner: started by a session that is gone, or a port no session claims. List them; do not kill them.
- Committed-but-unpushed or pushed-but-unmerged work per project.

## Root cause before remedy

A finding is a symptom. Before proposing any change, take each one a level down:
- **Root cause**, with evidence: why it happened, not that it happened.
- **Class**: harness (recurs in any project under the current setup), local (one project, session or episode), or already fixed (the cause changed after the data was recorded). Measure only data after the last relevant change, split by session start.
- **Worth fixing**: its cost per week now against the fix's own cost. A new rule, gate or nudge costs tokens every turn, blocks falsely and rots. "Leave it" is a valid answer.

Propose a change only for a harness cause that is still happening and worth it, at the root, never a patch on the symptom.

## Report to the owner

In the owner's language and style, conclusion first:
1. A one-line verdict: running ok or not, and the single biggest problem.
2. Findings ranked by cost to the owner (money, wrong answers, their time). Each gives what happened, how often, the evidence, its root cause and class, and either the proposed change or why to leave it.
3. What was not checked, and why.

Open a record for each finding the owner approves. Change nothing they have not approved.
