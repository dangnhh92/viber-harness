# Provenance

Where each rule came from, and why each upstream rule that is not here was dropped. Read this before adding, changing or removing a rule.

## Contents
- How to read the tables
- Rules with no upstream skill source
- Errors found upstream
- impeccable: SKILL.md
- impeccable: reference files with rules
- impeccable: workflow reference files
- taste-skill
- frontend-design
- Vercel Web Interface Guidelines

## How to read the tables

`source:line | upstream rule (paraphrased) | result`
- `-> ID`: kept as that rule (possibly reworded or merged).
- `dropped: reason`: not carried over. The usual reasons:
  - **not checkable**: no pass/fail test exists for it.
  - **taste**: a style preference, not a quality bar; a project may adopt it in its own rules.
  - **method**: how to build, not what must hold.
  - **tooling**: commands, scripts or setup of the upstream skill.
  - **conflict**: contradicts a kept rule; the kept rule is named.
  - **out of scope**: server, security or memory work, not interface design.

Copies mapped: impeccable SKILL.md (152 lines) and its 35 `reference/*.md` files (6081 lines); taste-skill SKILL.md (1206 lines); frontend-design `skills/frontend-design/SKILL.md` (42 lines); Vercel Web Interface Guidelines by section. Line numbers refer to those copies and shift when upstream changes.

## Rules with no upstream skill source

Restated from a public standard, or plain craft:
- S1, S4: plain craft (follow the given reference; ask one question on uncovered user-facing behaviour).
- F1: plain craft; taste-skill 4.8 and 4.9 agree on fake screenshots and fake-precise numbers.
- F2: plain craft.
- F3: WCAG 2.2 SC 1.4.3 applied to accent colours.
- F5: Apple Human Interface Guidelines (44 pt); WCAG 2.2 SC 2.5.8 (24 px).
- F6: Nielsen, response-time limit of 0.1 s; Apple HIG, Playing haptics.
- F7, F8: plain craft.
- HS1: house style; impeccable SKILL.md:98 and taste-skill 9.G hold the same ban.
- HS2: Microsoft Writing Style Guide, Capitalization.
- U20: Material Design 2, Dark theme.
- U24: web.dev, Cumulative Layout Shift.
- U29: WCAG 2.2 SC 2.5.1, 2.5.7.
- U35: WCAG 2.2 SC 1.1.1, 2.4.4.
- B4: WCAG 2.2 SC 1.4.2.
- data-display.md: every rule cites its own published source.

## Errors found upstream

- impeccable `typography.md:154` says body text under 16 px "fails WCAG on mobile". WCAG 2.2 sets no minimum font size. U21 keeps 16 px as a `[default]`, not as a WCAG claim.
- impeccable `color-and-contrast.md:51` defines large text as "18px+ or 14px bold". WCAG defines it as 18 pt (24 px) or 14 pt bold (18.66 px). U1 uses the WCAG figures.

## impeccable: SKILL.md

| source:line | upstream rule | result |
|---|---|---|
| SKILL.md:8-43 | load PRODUCT.md and DESIGN.md through `load-context.mjs`; pick a register | register -> S2; rest dropped: tooling |
| SKILL.md:47 | vary across projects; "GPT is capable" | dropped: not checkable |
| SKILL.md:51 | use OKLCH, reduce chroma at extremes | dropped: method |
| SKILL.md:52 | never `#000` or `#fff`; tint neutrals | dark surface part -> U20; `#fff` ban and tinting dropped: taste |
| SKILL.md:53-58 | name a colour strategy (restrained, committed, full palette, drenched) | -> U4 |
| SKILL.md:62-66 | theme from a physical scene sentence | -> S3 |
| SKILL.md:70 | body line length 65-75ch | -> U5 |
| SKILL.md:71 | type steps ratio 1.25 or more | -> U6 (brand value) |
| SKILL.md:75 | vary spacing for rhythm | dropped: not checkable |
| SKILL.md:76 | cards only when best; nested cards always wrong | -> U9 |
| SKILL.md:77 | don't wrap everything in a container | dropped: not checkable |
| SKILL.md:81 | don't animate layout properties | -> U14 |
| SKILL.md:82 | exponential ease-out; no bounce, no elastic | no bounce -> U14; curve choice dropped: taste |
| SKILL.md:88 | no side-stripe borders | -> U10 |
| SKILL.md:89 | no gradient text | -> U10 |
| SKILL.md:90 | no glassmorphism as default | -> B2 |
| SKILL.md:91 | no hero-metric template | -> B2 |
| SKILL.md:92 | no identical card grids | -> B2 |
| SKILL.md:93 | modal as first thought | dropped: not checkable |
| SKILL.md:97 | no restated headings or intros | -> U16 |
| SKILL.md:98 | no em dashes, no `--` | -> HS1 |
| SKILL.md:102 | "AI slop test" | dropped: not checkable |
| SKILL.md:104 | category-reflex check | -> B1 |
| SKILL.md:106-152 | command table, routing, pin and unpin | dropped: tooling |

## impeccable: reference files with rules

### product.md

| source:line | upstream rule | result |
|---|---|---|
| product.md:13 | system fonts are legitimate | dropped: a permission, not a rule |
| product.md:14 | one family is often right | dropped: taste |
| product.md:15 | fixed rem scale, no fluid type | -> P9 |
| product.md:16 | step ratio 1.125-1.2 | -> U6 (product value) |
| product.md:17 | prose 65-75ch, tables denser | -> U5 |
| product.md:23 | state-rich vocabulary | -> U11 |
| product.md:24 | accent for primary action, selection, state only | -> P3 |
| product.md:25 | second neutral layer for panels | dropped: taste |
| product.md:29-31 | predictable grids, familiar patterns, structural responsiveness | -> P1 |
| product.md:37 | skeletons, not centred spinners | -> U12 |
| product.md:38 | empty states that teach | -> U12 |
| product.md:39 | consistent affordances | -> P2 |
| product.md:43 | 150-250 ms transitions | -> U14 |
| product.md:44 | motion conveys state | -> U14 |
| product.md:45 | no orchestrated page-load sequences | -> U14 (folded: motion conveys state) |
| product.md:49 | no decorative motion | -> U14 |
| product.md:50 | inconsistent component vocabulary | -> P2 |
| product.md:51 | display fonts in labels, buttons, data | -> P8 |
| product.md:52 | reinventing standard affordances | -> P1 |
| product.md:53 | full saturation on inactive states | -> P3 |
| product.md:59-62 | permissions: system fonts, standard nav, density, consistency | dropped: permissions, not rules; consistency -> P2 |

### brand.md

| source:line | upstream rule | result |
|---|---|---|
| brand.md:13 | name an aesthetic reference first | -> S1 in spirit; the lane naming dropped: taste |
| brand.md:21-30 | font selection procedure and reflex-reject font list | dropped: taste; conflicts with a project's own fonts |
| brand.md:36-39 | font pairing by sector | dropped: taste |
| brand.md:47, 63 | fluid `clamp()` type and spacing | dropped: allowed for brand, not a rule (P9 bans it for product only) |
| brand.md:55-58 | name a palette reference; don't converge across projects | dropped: not checkable |
| brand.md:62, 64-65 | asymmetry or strict grid; don't center everything | dropped: taste |
| brand.md:66 | auto-fit card grid | dropped: method |
| brand.md:70-77 | use Unsplash stock when no local assets | dropped: conflict with F1 |
| brand.md:77 | alt text is part of the voice | -> U35 |
| brand.md:83 | one orchestrated page load | dropped: taste (U14 allows it for brand) |
| brand.md:84 | animate `grid-template-rows`, not `height` | -> U14 (only transform and opacity animate) |
| brand.md:88-90 | lazy monospace, rounded icons above headings, reflex single family | dropped: taste |
| brand.md:91 | no all-caps body copy | -> U22 |
| brand.md:92-94 | timid palettes; zero imagery; reflex editorial look | dropped: not checkable or taste |
| brand.md:100-104 | permissions: ambitious motion, typographic risk | dropped: permissions, not rules |

### color-and-contrast.md

| source:line | upstream rule | result |
|---|---|---|
| color-and-contrast.md:15, 70 | tinted neutrals | dropped: taste |
| color-and-contrast.md:36-42 | 60-30-10 distribution | -> U4 (restrained strategy) |
| color-and-contrast.md:51 | contrast table | -> U1, with the large-text figure corrected (see Errors found upstream) |
| color-and-contrast.md:55 | placeholder text 4.5:1 | -> U1 |
| color-and-contrast.md:60-66 | dangerous combinations (grey on colour, red/green) | -> U1, U3 |
| color-and-contrast.md:86-93 | dark mode is not inverted light mode | not-pure-black -> U20; the rest dropped: method |
| color-and-contrast.md:97 | token hierarchy | -> F4 |
| color-and-contrast.md:99 | heavy alpha is a smell | dropped: taste |

### typography.md

| source:line | upstream rule | result |
|---|---|---|
| typography.md:7 | vertical rhythm | dropped: taste |
| typography.md:13 | five-size system | dropped: taste |
| typography.md:29 | light text on dark needs spacing and weight compensation | dropped: taste |
| typography.md:31 | paragraph spacing | dropped: taste |
| typography.md:55 | don't pair similar fonts | dropped: taste |
| typography.md:57-90 | font loading, `font-display`, metric overrides | -> B3, V3 |
| typography.md:100-102 | `clamp()` only for brand headings, max 2.5x | product half -> P9; bound dropped: brand only |
| typography.md:112 | tabular numbers for data | -> U7 |
| typography.md:133 | `text-wrap: balance` | dropped: taste |
| typography.md:142 | all-caps tracking 0.05-0.12em | -> U22 |
| typography.md:146 | semantic token names | -> F4 |
| typography.md:152 | never disable zoom | -> U19 |
| typography.md:154 | 16 px body minimum | -> U21 as `[default]`; WCAG claim rejected |
| typography.md:155 | touch targets | -> F5 |
| typography.md:159 | two to three families at most | -> B3 |

### spatial-design.md

| source:line | upstream rule | result |
|---|---|---|
| spatial-design.md:7 | 4 pt base unit | dropped: taste |
| spatial-design.md:21 | squint test | dropped: not checkable |
| spatial-design.md:46 | cards are not required; never nest | -> U9 |
| spatial-design.md:50 | container queries | dropped: method |
| spatial-design.md:74 | optical adjustments | dropped: taste |
| spatial-design.md:78 | touch targets | -> F5 |
| spatial-design.md:96 | semantic z-index scale | -> F4 |

### layout.md

| source:line | upstream rule | result |
|---|---|---|
| layout.md:1-99 | layout workflow | dropped: method |
| layout.md:105 | nested cards | -> U9 |
| layout.md:106 | identical card grids | -> B2 |
| layout.md:107 | centering everything | dropped: taste |
| layout.md:108 | hero-metric template | -> B2 (real data in a hero is allowed) |
| layout.md:110 | arbitrary z-index values | -> F4 |
| layout.md:123-141 | live-mode parameters | dropped: tooling |

### motion-design.md

| source:line | upstream rule | result |
|---|---|---|
| motion-design.md:7-12 | 100/300/500 ms duration table | dropped: U14 uses 150-250 ms for product |
| motion-design.md:14 | exits at 75% of entrance duration | dropped: taste |
| motion-design.md:39 | no bounce or elastic | -> U14 |
| motion-design.md:43 | animate transform and opacity only | -> U14 |
| motion-design.md:47 | cap stagger total time | -> U14 (900 ms `[default]`) |
| motion-design.md:49-75 | reduced motion | -> U15 |
| motion-design.md:81 | 80 ms perception threshold | dropped: F6 uses Nielsen's 100 ms |
| motion-design.md:87 | optimistic UI | -> P10 |
| motion-design.md:95 | IntersectionObserver for scroll effects | -> U32 |

### interaction-design.md

| source:line | upstream rule | result |
|---|---|---|
| interaction-design.md:5-18 | eight interactive states | -> U11 |
| interaction-design.md:20-41 | visible focus ring 3:1; no bare `outline: none` | -> U2, U11 |
| interaction-design.md:45 | placeholder is not a label; validate on blur | -> U18, P7 |
| interaction-design.md:49 | optimistic UI; skeletons | -> P10, U12 |
| interaction-design.md:51-85 | `inert`, `<dialog>`, popover API | dropped: method |
| interaction-design.md:89, 155 | dropdowns clipped by overflow | -> V4 (screenshot check) |
| interaction-design.md:156 | z-index scale | -> F4 |
| interaction-design.md:161 | undo over confirm | -> U13 |
| interaction-design.md:165-177 | roving tabindex | -> V5 |
| interaction-design.md:181 | skip links | -> V5 |
| interaction-design.md:183-191 | gestures need a visible alternative | -> U29 |

### responsive-design.md

| source:line | upstream rule | result |
|---|---|---|
| responsive-design.md:5 | mobile first | dropped: method |
| responsive-design.md:9 | content-driven breakpoints | dropped: taste |
| responsive-design.md:13-37 | input method from pointer and hover queries; hover never required | -> U28 |
| responsive-design.md:39-59 | safe-area insets | -> U8 |
| responsive-design.md:62-93 | `srcset` and responsive images | -> V3 (LCP) |
| responsive-design.md:98 | adapt navigation and tables | -> U26, U30 |
| responsive-design.md:110 | test on real devices | -> V4, F7 |

### ux-writing.md

| source:line | upstream rule | result |
|---|---|---|
| ux-writing.md:5-17 | no OK, Submit or Yes/No; verb plus object | -> U33, U16 |
| ux-writing.md:21-35 | error formula; don't blame the user | -> U16 |
| ux-writing.md:39 | empty states teach | -> U12 |
| ux-writing.md:43 | consistent voice | dropped: not checkable |
| ux-writing.md:53 | no humour in errors | -> U16 |
| ux-writing.md:57 | standalone link text; informative alt; `alt=""` for decoration | -> U35 |
| ux-writing.md:63-74 | translations expand; avoid fixed widths | -> V7 |
| ux-writing.md:76-87 | one term per thing | -> U34 |
| ux-writing.md:91 | redundant copy | -> U16 |
| ux-writing.md:95 | specific loading text | -> U12 |
| ux-writing.md:99 | confirmation labels name the action | -> U13, U33 |
| ux-writing.md:103 | form instructions | dropped: taste |

### cognitive-load.md

| source:line | upstream rule | result |
|---|---|---|
| cognitive-load.md:39-52 | cognitive-load scoring | dropped: a scoring method, not pass/fail |
| cognitive-load.md:66 | navigation of 5 items or fewer | dropped: taste |
| cognitive-load.md:68, 94 | one primary action per view | -> P11 |
| cognitive-load.md:69 | at most 4 headline numbers | -> data-display L5 `[default]` |
| cognitive-load.md:70 | pricing of 3 tiers or fewer | dropped: taste |
| cognitive-load.md:84-86 | show current location | -> P12 |
| cognitive-load.md:90 | no unexplained jargon | -> U16, data-display N7 |

### harden.md

| source:line | upstream rule | result |
|---|---|---|
| harden.md:81 | 14 px minimum on mobile | -> U21 |
| harden.md:81 | use `clamp()` for responsive text | dropped: conflict with P9 for product |
| harden.md:88-91 | containers grow with text, no fixed widths | -> V7 |
| harden.md:101-110 | right-to-left layout | dropped: out of scope unless the product ships an RTL locale |
| harden.md:112-116 | long and unusual text | -> V7 |
| harden.md:130-136 | plurals through i18n | -> U17 |
| harden.md:141-146 | errors offer a retry | -> U12 |
| harden.md:158-163 | form error handling; keep input | -> P7 |
| harden.md:165-178 | API failure handling and degradation | dropped: out of scope (server) |
| harden.md:197 | long lists | -> P5 |
| harden.md:203 | prevent double submit | -> P7, V7 |
| harden.md:208-212 | explain missing permission | -> P13 |
| harden.md:222-233 | validation and security | dropped: out of scope |
| harden.md:252-278 | keyboard and screen reader | -> V5, U3, U18 |
| harden.md:288-299 | memory leaks | dropped: out of scope |
| harden.md:323-331 | NEVER list: silent failure, blank page on error | -> U12 |
| harden.md:337-345 | stress test inputs | -> V7 |

### polish.md

| source:line | upstream rule | result |
|---|---|---|
| polish.md:5-156 | polish workflow | dropped: method; concrete checks mapped below |
| polish.md:106-107 | one icon family, consistent sizes | -> U25 |
| polish.md:110 | images keep aspect ratio, no layout shift | -> U24 |
| polish.md:150, 176, 180 | no console logs or errors | -> V8 |
| polish.md:185-190 | NEVER list on polish process | dropped: method |
| polish.md:191 | hard-coded values instead of tokens | -> F4 |

### audit.md

| source:line | upstream rule | result |
|---|---|---|
| audit.md:5-58 | audit scan areas | -> verify.md V1 to V8 |
| audit.md:61-80 | health score | dropped: a scoring method, not pass/fail |
| audit.md:85-89 | P0-P3 severity | -> SKILL.md section 7 |
| audit.md:128-132 | report impact; verify before reporting | -> section 7 (evidence column) |

### onboard.md

| source:line | upstream rule | result |
|---|---|---|
| onboard.md:5-212 | onboarding workflow and principles | dropped: method |
| onboard.md:214, 220 | onboarding is skippable; Skip is visible | -> P14 |
| onboard.md:216 | dismissed tips stay dismissed | -> P14 |
| onboard.md:221 | returning users don't see first-run onboarding | -> P14 |
| onboard.md:215, 217-219 | don't patronise; don't block UI; no detached tutorial | dropped: not checkable |

### adapt.md

| source:line | upstream rule | result |
|---|---|---|
| adapt.md:8-168 | adaptation workflow | dropped: method |
| adapt.md:170 | don't hide core functions on mobile | -> U30 |
| adapt.md:171-176 | landscape, content breakpoints, touch on desktop | dropped: method or taste; touch on desktop covered by U28 |

### optimize.md

| source:line | upstream rule | result |
|---|---|---|
| optimize.md:3-189 | optimisation workflow | dropped: method |
| optimize.md:190-218 | LCP, INP, CLS thresholds | -> V3 |
| optimize.md:242 | `will-change` everywhere | dropped: method |
| optimize.md:243 | don't lazy-load above the fold | -> V3 (LCP) |

### typeset.md

| source:line | upstream rule | result |
|---|---|---|
| typeset.md:94 | two to three families | -> B3 |
| typeset.md:95 | commit to a scale | -> U6, P9 |
| typeset.md:96 | body text 16 px or more | -> U21 |
| typeset.md:97 | no display font for body | -> P8 |
| typeset.md:98 | never disable zoom | -> U19 |
| typeset.md:99 | font sizes in rem | -> U21 |
| typeset.md:100-101 | default fonts; similar pairs | dropped: taste |

### animate.md

| source:line | upstream rule | result |
|---|---|---|
| animate.md:154 | no bounce or elastic | -> U14 |
| animate.md:155 | animate transform, not layout | -> U14 |
| animate.md:156 | feedback under 500 ms | -> U14 (150-250 ms is tighter) |
| animate.md:157, 159 | animate with purpose; not everything | -> U14 |
| animate.md:158 | respect reduced motion | -> U15 |
| animate.md:160 | don't block interaction | -> U14 |

### clarify.md

| source:line | upstream rule | result |
|---|---|---|
| clarify.md:153, 159 | no unexplained jargon | -> U16, data-display N7 |
| clarify.md:154-155 | don't blame; don't be vague | -> U16 |
| clarify.md:156-157 | passive voice; long explanations | dropped: not checkable |
| clarify.md:158 | no humour in errors | -> U16 |
| clarify.md:160 | one term per thing | -> U34 |
| clarify.md:161 | no repeated information | -> U16 |
| clarify.md:162 | placeholder is not a label | -> U18 |

### overdrive.md and colorize.md

| source:line | upstream rule | result |
|---|---|---|
| overdrive.md:79, 118 | sound only after explicit opt-in | -> B4 |
| overdrive.md (rest) | push visual effects | dropped: taste |
| colorize.md:73, 100-101 | add gradients and blobs | dropped: taste; conflicts with B2 on purple gradients |
| colorize.md:132 | no purple-blue gradients | -> B2 |

## impeccable: workflow reference files

Dropped whole: these describe a command's procedure, not rules a screen must meet.

| file | reason |
|---|---|
| craft.md, shape.md | build workflow |
| teach.md, document.md, extract.md | context and design-system file generation (tooling) |
| live.md | browser variant mode with a long polling loop (tooling) |
| critique.md, heuristics-scoring.md, personas.md | scoring and persona review methods; not pass/fail |
| bolder.md, quieter.md, distill.md, delight.md | taste adjustments in one direction |

## taste-skill

| section (lines) | upstream rule | result |
|---|---|---|
| 0 (13-41) | read the brief; infer direction; audit first on redesigns | -> S1 to S4 |
| 0.D (38-41) | anti-default list | -> B2 |
| 1 (43-80), 7 (552-570) | variance and density dials | dropped: not checkable |
| 2 (82-120) | one design system per project; aesthetics table | one system -> P2; table dropped: taste |
| 3.A (126-133) | framework stack | dropped: framework-specific; font loading -> B3, V3 |
| 3.B | rendering choices | dropped: method; outcome checked by V3 |
| 3.C (140) | one icon family; preferred libraries | one family -> U25; library allow-list dropped: taste |
| 3.D | emoji rules | dropped: taste |
| 3.E | `dvh` over `100vh`; grid over flex maths | dvh -> U23; grid dropped: method |
| 3.F | dependency check | dropped: out of scope |
| 4.1 (165-183) | typeface bans and serif discipline | dropped: taste; clipped descenders -> V4 |
| 4.2 (185-207) | one accent; banned purple; premium palette bans | one accent -> U4, P3; purple -> B2; palette bans dropped: taste |
| 4.3 | avoid centred layouts | dropped: taste |
| 4.4 (213-217) | no nested cards; consistent radius; tinted shadows | -> U9, F4; tinted shadows dropped: taste |
| 4.5 (219-228) | button states, pressed feedback, contrast, no wrapping, no duplicate intent | -> U11, U12, F6, U1, U2, U27, U34 |
| 4.6 (230-232) | label above input, error below | -> P7, U18 |
| 4.7 (234-260) | CTA above the fold; nav on one line; eyebrow overuse; bento cell count; layout repetition | -> B5, U26, B2, F1; repetition, zigzag, nav height dropped: taste; mobile collapse -> U8 |
| 4.8 (262-296) | image generation first; picsum placeholders; logo walls; no div-built fake screenshots | fake screenshots -> F1; image generation and picsum dropped: conflict with F1; logo walls dropped: taste |
| 4.9 (298-331) | word counts; copy self-audit; no fake-precise numbers; one register | self-audit -> V8; fake numbers -> F1; word counts and register dropped: taste |
| 4.10 (333-339) | quotes of 3 lines or fewer; real attribution; no em dash | attribution -> F1; em dash -> HS1; length dropped: taste |
| 4.11 (341-350) | no theme flip mid-page | -> B6 |
| 5 (352-508) | motion recipes and library skeletons | motivated motion -> U14; recipes dropped: tooling; marquee cap dropped: taste |
| 5.D (509-517) | no raw scroll listeners | -> U32 |
| 6.A, 6.B | transform and opacity only; reduced motion | -> U14, U15 |
| 6.C, 6.F | tokens; z-index scale | -> F4 |
| 6.D, 6.E | font and image performance | -> V3 |
| 8 (572-593) | dark mode tokens; test both themes; no pure black | -> F4, V4, U20 |
| 9.A (599-605) | custom cursors | -> B2 |
| 9.B, 9.C | generic names; messy invented numbers | dropped: conflict with F1 (no invented content at all) |
| 9.D | filler verbs | -> B7 |
| 9.E | picsum images | dropped: conflict with F1 |
| 9.F (630-683) | decorative status dots; scroll cues; section-number eyebrows | status dots -> B2; rest dropped: taste |
| 9.G (685-703) | dash ban | -> HS1 |
| 10 | vocabulary list | dropped: not rules |
| 11 (783-833) | redesigns keep URLs, ids, labels, legal copy | -> U31 |
| 12 | block library | dropped: tooling |
| 13 | out-of-scope list | dropped: not rules |
| 14 (910-985) | pre-flight checklist | each item maps to the rows above |
| Appendices A-C (987-1206) | reference links | dropped: not rules |

## frontend-design

| source:line | upstream rule | result |
|---|---|---|
| SKILL.md:13-19 | design thinking: purpose, tone, constraints | -> S2, S3; "pick an extreme" dropped: not checkable |
| SKILL.md:21-25 | production-grade, functional code | -> verify.md |
| SKILL.md:30 | avoid Arial and Inter; pair display with body | font ban dropped: taste, conflicts with impeccable product.md:13; pairing -> B3 |
| SKILL.md:31 | CSS variables; one dominant colour | -> F4, U4 |
| SKILL.md:32 | staggered page-load reveal; surprising hover | stagger -> U14 (brand); surprise dropped: taste |
| SKILL.md:33 | unexpected spatial composition | dropped: taste |
| SKILL.md:34 | textures, grain, custom cursors | dropped: taste; custom cursors conflict with B2 |
| SKILL.md:36 | no purple gradients on white; avoid overused fonts | gradients -> B2; fonts dropped: taste |
| SKILL.md:38-42 | vary every time; "Claude is capable" | dropped: not checkable |

## Vercel Web Interface Guidelines

Mapped by section; bullets are paraphrased.

| section | result |
|---|---|
| Accessibility | -> U18, U35 |
| Focus States | -> U11 |
| Forms | -> P7, U18 |
| Animation | -> U14, U15 |
| Typography | -> U7 |
| Content Handling | -> P6 |
| Images | -> U24 |
| Performance | -> P5, B3 |
| Navigation and State | -> P4, U13 |
| Touch and Interaction | -> F5, U28 |
| Safe Areas and Layout | -> U8 |
| Dark Mode and Theming | -> F4, U20 |
| Locale and i18n | -> U17, data-display N6 |
| Content and Copy | -> U12, U16 |
| Anti-patterns | -> U19, U14, U11 |
| Hover and Interactive States | -> U11, U28 |
| Hydration Safety | dropped: framework-specific |
