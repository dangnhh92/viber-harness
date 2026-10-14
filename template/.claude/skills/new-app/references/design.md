# Design: mobile additions to designing-interfaces

## Contents
- UI/UX and HIG layout
- Motion and haptics
- Accessibility and small screens
- Onboarding

UI: load `designing-interfaces` first. It owns:
- references and copy;
- placeholders;
- contrast;
- touch targets;
- safe areas;
- nested cards;
- destructive confirm;
- empty, loading and error states (skeletons);
- base motion timing and reduced motion;
- shipping-engine screenshots;
- onboarding skip.

This file holds only the mobile rules it does not state. Where this file overrides it, the line says so.

## UI/UX and HIG layout

**Needed when:** every screen.

**Not needed when:** never skipped. A game's play field may break platform conventions; its menus and sheets still follow them [invented].

**Do it right:**
- Any text change ships with a string-by-string reference table (old, new, where).
- Build every rule configurable from the first prototype.
- Test every screen with a notch present [HIG-layout].
- If the app shows a banner ad, keep banner height plus the safe-area inset clear on every screen: no menu, overlay or card underneath it.
- Sheets add the bottom safe-area inset (`insets.bottom`).
- Every form screen sits in a keyboard-avoiding container.
- Inventory every popup, toast and icon; check each for meaning and consistency.
- Destructive actions are styled as destructive (never brand primary) and always have a cancel.
- Every toast or snackbar auto-dismisses. Flutter: a `SnackBar` with an action needs `persist: false` and a duration (about 2.5 s).
- Every screen change hides the previous screen's overlays. A tutorial or overlay must never render under another layer.
- Add a release-build guard that fails on any user-facing string in the wrong language (developer or debug screens included).
- Anti-AI-look additions for app screens [Impeccable]:
  - No gray text on coloured backgrounds.
  - No purple-to-blue gradients.
  - Tint neutrals; never pure black or pure gray, light mode included.

**Check:** Has every screen been captured with a notch and (if any) a banner present, with no control under them, and is there a reference table for every user-facing string?

## Motion and haptics

**Needed when:**
- Every tappable element: a press state.
- Every outcome: success, error or refusal.
- Every screen entrance and list load.

**Not needed when:**
- Frequent, standard interactions the system already animates [HIG-motion].
- Constant idle motion, confetti or wobble: never.

**Do it right:**
- One motion module per app, imported everywhere. Standard values:
  - Spring `{stiffness: 150, damping: 16, mass: 1}`, damping ratio about 0.65.
  - `STAGGER_MS = 70`
  - `LEAD_MS = 150`: the picture lands before its text.
  - `FEEDBACK_MS = 120`, ceiling 300 ms for press, toast and state change.
  - `ENTRANCE_MS = 600`, ceiling 900 ms.
  - `TOAST_HOLD_MS = 1800`
  - `BANNER_HOLD_MS = 4000`
- Native mobile entrances use one spring (damping ratio 0.65, slight overshoot, never a wobble), matching platform motion. This overrides designing-interfaces U14 "no bounce" for native app entrances only; product transitions still follow U14.
- Press feedback is not a transition: it uses `FEEDBACK_MS = 120` (ceiling 300 ms). Screen and state transitions follow designing-interfaces U14 (150 to 250 ms).
- Enforce the budgets with a test (for example `motion.test.mjs`): feedback at most 300 ms, entrance at most 900 ms, exactly one spring. A ceiling nobody enforces is a comment.
- Entrance choreography:
  - Anticipation, then a sprung move, then a settle.
  - Order: art, title, hint, card, 60 to 90 ms apart, done in about 900 ms.
  - Afterwards only a slow breathe loops.
  - Everything runs on the native driver.
- Drive launch and entrance animation from one native clock. JS timers (`Animated.delay`) start tracks late.
- Lists:
  - The skeleton does not loop forever.
  - Stagger on first load only, never on refresh.
  - Pull-to-refresh in the brand colour.
- Celebrate a milestone with one small success moment, never confetti.
- When a newer motion rule replaces an older one, close the old rule in the same change.
- Haptics map to meaning and stay consistent [HIG-haptics]:
  - `Light` impact on copy.
  - `Success` notification when a submit completes a task (HIG: success feedback for a finished task); a light impact for minor commits (designing-interfaces F6).
  - `Warning` on every refusal or error.
- At most one haptic per gesture; a double buzz is a defect.
- Pair each haptic with the matching visual, matched in intensity and sharpness [HIG-haptics].
- Haptics can be turned off: a Settings toggle, on by default [HIG-haptics].
- Guard every native module import (haptics, review, and similar) so an OTA update reaching an older binary degrades to silence instead of crashing. Lazy-import it.
- Reduce Motion, beyond designing-interfaces U15:
  - Entrances show their end state.
  - Haptics still fire.
  - Screen shake is off.
  - Read the setting as `boolean | null`; hold entrances at their start pose while it is null, so no first frames flash.
  - Never await the setting with no timeout before the splash leaves; a promise that never settles keeps the splash up.
- After a scripted find-and-replace fix, verify the anchor matched and the new branch can fire. A replace that matched nothing ships a no-op.
- Android without a shared RN module: M3 durations from `short1` (50 ms) to `extraLong4` (1000 ms); emphasized decelerate `cubic-bezier(0.05, 0.7, 0.1, 1)` to enter, emphasized accelerate `cubic-bezier(0.3, 0, 0.8, 0.15)` to exit [M3-motion].
- Games hold a steady 60 fps on the smallest supported phone (HIG floor is 30 to 60 fps steady) [HIG-motion].
- Report motion work as a plain list. No videos unless the owner asks.

**Check:** Does the motion module exist with a passing budget test (feedback at most 300 ms, entrance at most 900 ms, one spring)? Does a Reduce Motion run show final frames with no entrance flash and haptics still firing?

## Accessibility and small screens

**Needed when:** always, every app.

**Do it right:**
- Touch target absolute minimum on iOS is 28x28 pt [HIG-a11y]. Measure targets in points, not pixels (120 px is under 44 pt on an SE).
- Padding about 12 pt around bezelled controls, 24 pt around unbezelled ones [HIG-a11y].
- Contrast thresholds follow designing-interfaces U1 (WCAG: 3:1 only from 24 px, or 18.66 px bold). The stricter bar wins.
- A full-page overlay (grain, texture) can make automated a11y tools report zero violations falsely. Test without it.
- Support Dynamic Type up to 200%. Use `minHeight`, never fixed `height`, on buttons, chips and badges [HIG-a11y].
- Lay out and measure at three iPhone sizes: 375x667 (SE), 390x844, 430x932.
- Grids and games also test 320, 360, 375, 390 and 430 pt widths, and keep at least 690 pt on the iPad short side.
- Compress on short frames, spread on tall ones (shrink hero art on SE; no dead bands on large phones).
- Never convey information by motion alone; pair it with haptics or audio [HIG-motion; HIG-a11y].
- Before recording a platform behaviour as fact, read the platform source for the version in use.

**Check:** At 375x667 and at the largest Dynamic Type, is the primary action visible without scrolling, with no clipped label?

## Onboarding

**Needed when:** the app has a mechanic that cannot be learned by trying it, or needs a permission before it can work at all [HIG-onboarding].

**Not needed when:** the first screen can teach by doing. Prefer contextual tips over a slide deck [HIG-onboarding].

**Do it right:**
- Fast and fun. Skip and no-repeat: designing-interfaces P14. Once skipped, keep it findable in Settings [HIG-onboarding].
- Teach through interaction. No license text. Postpone setup; ship defaults [HIG-onboarding].
- No rating, purchase or permission ask before the person has experienced the app [HIG-onboarding].
- Slides: swipe in both directions, a back control from slide 2, tappable dots.
- Motion follows the motion section. The onboarding prototype is approved before the rest is built.
- First launch shows only the core action (Play, Settings). Unlock the rest as the person uses the app; a full menu on first launch overwhelms.
- The tutorial renders on top of everything; check z-order.

**Check:** Can onboarding be skipped, navigated backward, and reopened from Settings, and does it ask for nothing (rating, purchase, permission) before the first value moment?
