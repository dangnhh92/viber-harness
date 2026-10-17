---
name: device-testing
description: Drive and verify an app on a real iPhone, iOS Simulator, Android emulator or browser. Load before any UI test, capture, walkthrough or exploratory run on a device or browser.
---

# Device and browser testing

Tools: `agent-device` (MCP server `agent-device`, declared in `.mcp.json`, pinned 0.21.28) for real iPhone, Simulator and Android. Playwright for the browser. Never idb, AXe, or ad hoc `xcrun simctl io` taps. Do not write a custom XCUITest step driver for exploratory work; agent-device keeps its runner warm between steps.
What "tested" means, oracles, review conditions: `.claude/skills/new-app/references/store.md` (Testing). It wins where it differs.

## Setup (once per machine)
- Needs Node 22.12 or newer. `.mcp.json` starts the server with `npx -y agent-device@0.21.28 mcp`; approve the project MCP server when Claude Code asks. Run `npx -y agent-device@0.21.28 doctor` once and fix what it reports.
- Real iPhone: Xcode, the phone paired and trusted (cable once, then Wi-Fi works), Developer Mode on, and `AGENT_DEVICE_IOS_TEAM_ID` set to your Apple team id in the shell profile so the runner can be signed.
- Browser: the Playwright plugin or MCP server.
- Upgrade on purpose: bump the pinned version in `.mcp.json` and here together, then rerun `doctor`.

## Loop
1. Start with `open <app> --foreground` (add `--save-script <path>.ad` when the run may be replayed). No probing first.
2. Act with `press` / `fill` plus `--settle`; read the returned diff and decide from it. Re-snapshot only when the diff is empty or unexpected.
3. Verify each step with an assertion (`wait text`, `is`, `get`, `find`), not by looking.
4. `close` at the end; on Simulator it keeps the runner warm for the next run.

## Selecting elements
- Order: snapshot ref `@eN` (copy byte for byte), then id / accessibility label / role, coordinates last.
- Refs expire after any screen change: take them from the latest diff or snapshot.
- Prefer stable ids over visible text; text breaks under localization. A control you need with no id is a defect to report, not to work around silently.
- Browser: role and label locators (`getByRole`, `getByLabel`), never CSS chains or XPath.

## Waiting
- Never `sleep` or a fixed timeout. Wait on a condition: `wait 'label="X"' <ms>`, `wait text`, Playwright web-first assertions.
- `press` does not wait for its target; put an explicit `wait` before it when the target appears after load or animation.
- Scroll with `scroll down --until <selector>`, never a fixed count.
- Long operations (upload, sync, purchase): one wait with a generous bound (for example 30000 ms), then fail.

## Screenshots
- The text snapshot is the default read. Screenshot only when the snapshot is sparse (games, canvas, Flutter without semantics), two elements look the same in text, the plan asks for a capture, or a step failed.
- Look at every screenshot you take.

## System alerts and sheets
- Permission alerts: `alert wait`, then `alert accept|dismiss`. On `ALERT_BUTTON_NOT_FOUND` (non-English label): `snapshot -i`, then `press @ref`.
- Simulator: set permission state before launch when the alert itself is not under test: `xcrun simctl privacy <udid> grant|revoke|reset <service> <bundle>`.
- The StoreKit sheet and Apple Account prompts run in SpringBoard, not the app. Password fields there are reachable; secrets come from an env var or Keychain, never typed into a plan or log.
- The Face ID side-button confirm on a real iPhone cannot be automated: stop at it, ask a person for that one press, continue. A purchase without it is not passed.

## State between runs
- Simulator: `xcrun simctl erase <udid>` for review-condition runs; `settings clear-app-state` / `settings reset-keychain` for a quick reset.
- Real iPhone: those resets are unsupported. Uninstall and reinstall the app; a fresh sandbox tester per paywall run.
- Android: `adb shell pm clear <package>`.
- Browser: a new context per test; no shared login state unless the plan seeds it.
- Never depend on the previous run's leftovers. Seed data through the real ingest path.

## Record and replay
- An exploratory run that found the path: save it (`--save-script`), then replay it once (`replay <file>.ad`) before calling it a script. A script that never replayed clean is a note.
- Regression set: `agent-device test ./workflows --retries 1`. Export to Maestro YAML only when a plan asks.
- `REPLAY_DIVERGENCE` or a selector miss means the app changed or the script is wrong. Report it with the diff; never patch the script just to pass.
- Playwright planner or generator may draft browser tests; a healer that marks a test skipped is a failure, not a fix.

## Flakiness
- Retries follow the project's runner agent rules; without one, one plain retry, then record the step failed with its error text.
- A step that passes only on retry is reported flaky with both outcomes, never passed.
- Follow agent-device error hints before improvising; typed reasons (`signing_no_development_team`, `device_developer_mode_disabled`) go into the report verbatim.

## Real iPhone preconditions
- Paired, trusted, unlocked, Developer Mode on. A locked phone fails `open`; check first, and ask a person to unlock rather than retrying.
- The first `open` after an upgrade rebuilds and signs the runner (slow, once).

## Cleanup
- `close` every session; shut down simulators you booted and quit Simulator; kill only PIDs you started.
