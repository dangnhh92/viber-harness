# Verify before calling UI done

## Contents
- Loop and checklist
- V1 Contrast, computed
- V2 Lighthouse
- V3 Core Web Vitals
- V4 Screenshots in the shipping engine
- V5 Keyboard and reduced motion
- V6 Rule sweep
- V7 Stress inputs
- V8 Console and copy

## Loop and checklist

Copy this into the task. Run every step that applies to the change.

```
- [ ] V1 contrast computed, light and dark
- [ ] V2 Lighthouse, mobile and desktop, every touched page
- [ ] V3 Core Web Vitals within limits
- [ ] V4 screenshots captured in the shipping engine and looked at
- [ ] V5 keyboard pass and reduced-motion pass
- [ ] V6 rule sweep greps clean
- [ ] V7 stress inputs survive
- [ ] V8 no console errors; every visible string re-read
```

Feedback loop: run the list, fix every fail, then rerun the whole list (a fix can break an earlier step). Stop only when a full run has no fail.
Report each step as `step | result | evidence`. A skipped step is `not run` with the reason.
Values marked `[default]` have no published source; a project may override them. The person whose work is measured never sets or lowers a bar.

## V1. Contrast, computed

- Compute the WCAG contrast ratio for every text and background token pair the change uses, in light and dark. Text needs 4.5:1 (3:1 at 24 px, or 18.66 px bold); meaningful non-text needs 3:1. (WCAG 2.2 SC 1.4.3, 1.4.11)
- Accent colours used as text are the usual failure: orange `#F97316` on white measures 2.80:1; the darker `#C2410C` measures 5.18:1 (SKILL.md F3).
- Lighthouse does not check text over images, gradients or video, nor hover and focus states. Compute those by hand from the actual colours.

## V2. Lighthouse, on more than the home page

```
npx lighthouse@13.5.0 <url> --only-categories=accessibility,performance,best-practices,seo --output=json --output-path=<scratch>/lh-<page>-<form>.json --chrome-flags="--headless"
```

- Pin one Lighthouse version per project, so scores are comparable between runs.
- Run on the home page, at least one subpage, and every page the change touched. A passing home page says nothing about a subpage.
- Run mobile (the default) and desktop (`--preset=desktop`).
- Performance varies run to run: take the median of 3 runs before comparing with a bar. `[default]`
- Serve a production build, never a development server.
- Start the server yourself and stop it by the process id you started. Never stop processes by name pattern; other processes may be running.

Bars: accessibility 100 on every page run; mobile performance 90 or above. Best practices and SEO 100 `[default]`.

## V3. Core Web Vitals

- LCP 2.5 s or less, INP 200 ms or less, CLS 0.1 or less, at the 75th percentile. (web.dev, Web Vitals)
- Lab runs give LCP and CLS. INP needs field data; in the lab, use Total Blocking Time of 200 ms or less as the proxy. `[default]`

## V4. Screenshots, in the shipping engine

- Capture every changed screen at 390x844 and 1440x900, in light and dark. `[default]`
- Use the engine the screen ships in: WebKit (Playwright `webkit`) for an iOS app or iOS web view; the device or simulator for a native app. Chromium alone is not approval evidence. (SKILL.md F7)
- Look at every screenshot before reporting. Check: no horizontal scroll at 360 px (U8), no clipped or overlapping text, no dropdown or popover clipped by its container, every empty, loading and error state captured once (U12).

## V5. Keyboard and reduced motion (web)

- Tab through the changed screen: every control is reachable in a logical order and shows a visible focus ring. (WCAG 2.2 SC 2.1.1, 2.4.3, 2.4.7)
- Emulate `prefers-reduced-motion: reduce`: non-essential animation stops or shortens. (U15)

## V6. Rule sweep

- Grep the diff for U+2014 and U+2013 in UI strings and comments, unless the project overrides HS1.
- Grep the diff for hex colour literals outside the token file, and for `z-index` values not taken from the scale (F4).
- Grep for `transition: all`, `user-scalable=no`, `maximum-scale=1`, and `outline: none` without a replacement (U14, U19, U11).
- Grep UI strings for "OK", "Submit", "Click here" and "lorem" (U33, U35, F1).
- Walk the rule IDs in `SKILL.md` and, for data screens, `data-display.md`; report each as pass, fail or not checked.

## V7. Stress inputs

Load the changed screen with each input and confirm nothing overflows, overlaps, crashes or blanks:
- a name or title of 100+ characters with no spaces;
- diacritic-heavy text (Vietnamese, German) and CJK text;
- emoji in user-entered fields;
- 1000+ rows in any list or table (P5);
- empty data (U12);
- offline or a failed request (U12);
- a double-click on submit (P7);
- browser zoom at 200% (U19; WCAG 2.2 SC 1.4.4).

## V8. Console and copy

- The browser console shows no error and no warning on load and through the main flow.
- Re-read every visible string on the changed screen once, against U16, U33 to U35, HS1 and HS2.
- Optional: impeccable's anti-pattern detector (`npx impeccable@4.1.0`, flags in its `--help`) flags many section 4 and 6 bans automatically. Its findings are leads; the rule IDs decide.

Sources: addyosmani/web-quality-skills (MIT) for the audit order and Core Web Vitals thresholds; web.dev Web Vitals; Lighthouse CLI; WCAG 2.2.
