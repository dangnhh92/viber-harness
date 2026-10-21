---
name: designing-interfaces
description: Provides one pass/fail rule set for designing, building and reviewing user interfaces (web pages, app screens, admin consoles, landing pages) with a verification checklist. Use before writing UI code, choosing colour, type or layout, writing interface copy, or reviewing a screen. Adds data-display rules when a screen shows numbers, charts, tables, status or alerts.
---

# Designing interfaces

Every rule has an ID and is pass or fail on a rendered screen or its source.
"Looks fine" is not evidence. A number, a screenshot path or a `file:line` is.

Terms used throughout:
- **requester**: the person who asked for the work.
- **user**: a person who uses the finished screen.
- **screen**: one rendered view at one viewport size.
- **`[default]`**: a value with no published source; a project may override it in its own rules.

## Workflow

Copy this checklist into the task and tick it as you go:

```
- [ ] 1. Answer S1 to S4 in writing before any layout
- [ ] 2. Load what the table below says for this screen
- [ ] 3. Build or change the screen
- [ ] 4. Run references/verify.md; fix every fail; rerun until none is left
- [ ] 5. Report every rule ID checked as pass, fail or not checked (section 7)
```

## 0. What to load

| The work | Also read |
|---|---|
| The screen shows a number, chart, table, KPI, status or alert | [references/data-display.md](references/data-display.md) |
| Admin console, settings, tool, any signed-in task screen | section 5 |
| Landing page, personal site, store or marketing page | section 6 |
| Before calling any UI done | [references/verify.md](references/verify.md) |
| Changing or auditing this skill's rules | [references/provenance.md](references/provenance.md) |

If a charting skill with its own palette validator is installed, use it for chart marks and colour; `data-display.md` decides what to show.
Use one design rule set per task. Two skills with different rules produce averaged output.

## 1. Before designing

- **S1** Name the reference: the app or site the requester pointed to for this screen, or "none given". When one is given, layout and copy follow it before anything is invented.
- **S2** State the register in one line: `brand` (the design is the product) or `product` (the design serves a task).
- **S3** Write one scene sentence before choosing light or dark: who, where, what light, what mood. A category name ("dashboard") is not a scene.
- **S4** A user-facing behaviour or piece of copy the brief does not cover goes to the requester as one question, with your recommendation first. Technical calls stay with the builder.

## 2. Foundations (win over any rule below)

- **F1** Real assets only: no lorem ipsum, no placeholder image, no fake screenshot built from divs, no invented testimonial, logo or metric. A testimonial names a real person and role. A grid has no empty filler cell. An empty section beats a fabricated one.
- **F2** Show if present: an optional field renders only when it has a value. No "N/A", no empty label, no placeholder dash.
- **F3** An accent colour used as text must itself measure 4.5:1 on its background; otherwise the text goes neutral and the accent stays on the icon, fill or border. (WCAG 2.2 SC 1.4.3)
- **F4** Colour, spacing, radius, shadow and z-index values come from tokens. No hex literal outside the token file. Every colour token has a dark-mode value. Z-index uses a named scale; `999` and `9999` fail.
- **F5** Touch targets are at least 44x44 pt on mobile and never under 24x24 CSS px anywhere. (Apple Human Interface Guidelines; WCAG 2.2 SC 2.5.8)
- **F6** Every tap, press and submit shows visible feedback within 100 ms: a pressed state, then success or error. On mobile, commit actions add a light haptic. (Nielsen, "Response times: the 3 important limits", 0.1 s; Apple HIG, Playing haptics)
- **F7** Approval screenshots come from the engine that ships the screen (WebKit for an iOS web view, the device or simulator for a native app), never only Chromium.
- **F8** A diagram answers one question, labels every arrow in plain words, and colours nodes by role with a one-line legend.

## 3. House style (defaults; a project may override)

- **HS1** No em dash (U+2014) or en dash (U+2013) in UI strings, alt text or code comments. Use a comma, colon or parentheses.
- **HS2** Headings, buttons, labels and menu items use sentence case: first word and proper nouns capitalised. (Microsoft Writing Style Guide, Capitalization) Platforms whose guidelines use title case for some elements may override.

## 4. Core rules, every surface

Colour and contrast
- **U1** Text 4.5:1; large text (24 px, or 18.66 px bold) 3:1; measured against its actual background. Placeholder text included. (WCAG 2.2 SC 1.4.3)
- **U2** Icons, input borders, focus rings and chart marks that carry meaning: 3:1 against the adjacent colour. (WCAG 2.2 SC 1.4.11)
- **U3** Colour never carries meaning alone: a state also has an icon, text or shape. (WCAG 2.2 SC 1.4.1)
- **U4** Name the colour strategy: restrained (neutrals plus one accent on 10% of the surface or less), committed, full palette, or drenched. Product screens are restrained.
- **U20** Dark-mode surfaces are not pure `#000000`; the base surface is a dark grey such as `#121212`. (Material Design 2, Dark theme)

Type
- **U5** Prose line length is 65 to 75 characters. Tables may run wider.
- **U6** Adjacent type steps differ by a ratio of at least 1.125 (product) or 1.25 (brand). `[default]`
- **U7** Numbers that are compared or that update use `font-variant-numeric: tabular-nums`. (Vercel Web Interface Guidelines)
- **U21** Body text is at least 16 px; font sizes are set in `rem`; no text below 14 px on a phone. `[default]`
- **U22** All caps only on short labels, eyebrows and small headings, with `letter-spacing` 0.05em to 0.12em. Never on a sentence. (Microsoft Writing Style Guide, Capitalization)

Layout
- **U8** No horizontal page scroll at 360 px width. Content clears device safe areas (`env(safe-area-inset-*)`). (Vercel Web Interface Guidelines)
- **U9** No card inside a card.
- **U10** No coloured side-stripe border wider than 1 px on cards, list items or alerts. No gradient text.
- **U23** Full-height sections use `dvh` or `svh`, not `100vh`.
- **U24** Every image and embed reserves its box (width and height, or `aspect-ratio`), so loading shifts nothing. (web.dev, Cumulative Layout Shift)
- **U25** One icon family and one stroke width per product.
- **U26** Primary navigation fits one line at 1024 px or collapses into a menu.
- **U27** Button labels do not wrap at 1024 px and wider.
- **U37** Every screen has one lead element (largest, heaviest or first) so the eye has a place to start. Three or more equal-size sibling blocks fail, unless they are rows of like items (a list, table or gallery). A long list of like items surfaces one differentiator, such as recency or status.
- **U38** An empty state fills the viewport it sits in and names the next action. A small block under the header with blank space below it fails.
- **U42** A sticky or fixed header, footer or banner never fully covers the focused element. Set `scroll-padding-top` to the header height. (WCAG 2.2 SC 2.4.11)
- **U43** Body text is left-aligned, never justified.

States and interaction
- **U11** Every interactive component has default, hover, focus-visible, active, disabled and loading states. Focus is never removed without a visible replacement. (Vercel Web Interface Guidelines; WCAG 2.2 SC 2.4.7)
- **U12** Every data region has a designed empty, loading and error state. Loading in content is a skeleton, not a centred spinner. An error says what failed and offers a retry. One failing region never blanks the page.
- **U13** A destructive action has a confirm step or an undo window. Initial focus in a destructive confirm goes to Cancel, never to the destructive button. (Vercel Web Interface Guidelines)
- **U28** Hover is never the only way to reach a function or a piece of information.
- **U29** Every gesture (swipe, long press, drag) has a visible control that does the same thing. (WCAG 2.2 SC 2.5.1, 2.5.7)
- **U30** The mobile layout keeps every function the desktop layout has.
- **U31** A redesign keeps URLs, anchor ids, navigation labels, form field names, analytics ids and legal copy unless the requester approved the change.
- **U36** A modal dialog takes focus on open, keeps Tab and Shift+Tab inside, closes on Escape, and returns focus to the control that opened it. It has an accessible name. A native `<dialog>` opened with `showModal()` meets this. (WCAG 2.2 SC 2.1.2, 2.4.3)
- **U39** A control that declares state (`aria-pressed`, `aria-expanded`, `aria-sort`, `aria-checked`, `aria-selected`) changes that state on click or key press, and its look changes with it. An attribute that flips while the render stays identical fails.
- **U40** A success message appears only when the visible data changed too. A "created" toast over an unchanged list fails.
- **U41** A region that scrolls sideways shows it: an edge fade, a visible scrollbar or an arrow.

Motion
- **U14** Motion conveys a state change. Product transitions run 150 to 250 ms; staggered entrances finish within 900 ms `[default]`. Only `transform` and `opacity` animate. No `transition: all`. No bounce or elastic easing. Animation never blocks input. (Vercel Web Interface Guidelines)
- **U15** `prefers-reduced-motion: reduce` removes or shortens every non-essential animation. (WCAG 2.2 SC 2.3.3)
- **U32** Scroll-linked effects use IntersectionObserver or CSS scroll-driven animation, never a raw `scroll` listener that sets state on every event.

Copy
- **U16** Buttons name the action ("Save changes", not "Continue"). Errors state cause and fix, never blame the user, and carry no jokes. No heading is restated in the first sentence below it. (Vercel Web Interface Guidelines)
- **U17** Dates, numbers and plurals format through `Intl.DateTimeFormat`, `Intl.NumberFormat` and `Intl.PluralRules` (or the platform equivalent), never a hand-built string. (Vercel Web Interface Guidelines)
- **U33** No "OK", "Submit" or "Yes"/"No" as a button label. A destructive button names its object and count ("Delete 3 files").
- **U34** One term per thing across the product, and one label per intent: two buttons that do the same thing carry the same words.
- **U35** Link text makes sense on its own ("View pricing", not "Click here"). Alt text states the information an image carries; decorative images have `alt=""`. (WCAG 2.2 SC 1.1.1, 2.4.4)

Semantics (web)
- **U18** Actions are `<button>`, navigation is `<a>`. No click handler on a `div`. Icon-only buttons have `aria-label`. Every input has a label. (Vercel Web Interface Guidelines; WCAG 2.2 SC 4.1.2)
- **U19** Zoom is never disabled: `user-scalable=no` and `maximum-scale=1` fail. (WCAG 2.2 SC 1.4.4)

## 5. Product and admin screens

- **P1** Standard patterns only: top bar or side navigation, tabs, breadcrumbs, tables, native form controls. No custom scrollbar or reinvented control.
- **P2** One component library and one component vocabulary: the same action looks the same on every screen.
- **P3** The accent marks the primary action, the current selection and state only. No decorative colour; inactive items are not fully saturated.
- **P4** Filters, tabs, sort and pagination live in the URL; a reload restores the view. (Vercel Web Interface Guidelines)
- **P5** Lists over 50 rows virtualise or paginate. `[default]` (Vercel Web Interface Guidelines)
- **P6** Long text truncates with the full value reachable (tooltip or detail view). (Vercel Web Interface Guidelines)
- **P7** Forms: label above the field, error below it. Errors appear on blur or submit, not on every keystroke. On a failed submit, focus moves to the first error and every entered value is kept. Submit stays enabled until the request starts, then is disabled until it settles. (Vercel Web Interface Guidelines; WCAG 2.2 SC 3.3.1)
- **P8** No display or decorative typeface in labels, buttons, tables or data.
- **P9** A fixed `rem` type scale; no `clamp()` font sizes.
- **P10** Optimistic updates only for low-stakes, reversible actions; never for payments or destructive actions.
- **P11** Each view has one primary action and at most two secondary actions at the same level.
- **P12** The current location is always visible: active navigation item, page title or breadcrumb.
- **P13** A control hidden or disabled for lack of permission says why, where the user would expect it.
- **P14** Onboarding has a visible skip, is not shown again to a returning user, and a dismissed tip stays dismissed.
- **P15** One action role, one variant: the destructive action wears the same danger style on its trigger and on its confirm button. Primary is the single main action. Secondary is never a coloured fill.
- **P16** Sign-in and verification fields allow paste and password managers (`autocomplete` set, no paste block). No step needs a puzzle, a transcription or a CAPTCHA without an alternative. A multi-step form never re-asks a value already entered. (WCAG 2.2 SC 3.3.7, 3.3.8)

## 6. Brand and landing pages

- **B1** The direction is not guessable from the category name alone ("finance, so navy and gold" fails).
- **B2** None of: identical icon, heading and text card grid; decorative glassmorphism; big-number hero with a gradient accent; purple gradient on white; custom cursor; a status dot that conveys no state; an uppercase eyebrow above more than one section in three.
- **B3** One display face plus one body face at most; both load with `font-display: swap`. (Vercel Web Interface Guidelines)
- **B4** No sound plays without a user action; audio starts only after opt-in. (WCAG 2.2 SC 1.4.2)
- **B5** The primary call to action is visible without scrolling at 1440x900 and 390x844. `[default]`
- **B6** No section flips between light and dark theme mid-page.
- **B7** No filler verbs or adjectives: "elevate", "seamless", "unleash", "next-gen", "revolutionize".
- **B8** The largest heading is at least 2.5x the body size and wraps to 3 lines or fewer. `[default]`

## 7. Review output

```
rule | result | severity | evidence
U1   | fail   | P1       | pricing card note #F97316 on #FFFFFF = 2.80:1 (src/pricing.tsx:41)
U12  | pass   |          | empty, loading, error captured (shots/orders-*.png)
D5   | not checked |     | no live data in the test build
```

Severity of a fail: **P0** blocks the task, **P1** major or a WCAG AA failure, **P2** minor with a workaround, **P3** polish.
A rule not checked is listed as `not checked` with the reason. It never counts as pass.

Sources and licences: [NOTICE.md](NOTICE.md).
