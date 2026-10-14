---
name: new-app
description: Provides the rules and a blocking pre-submit checklist for building and shipping a mobile app on iOS and Android (Expo/React Native, Flutter, native Swift or Kotlin). Use it whenever the user starts a new app, names or researches one for the stores, overhauls an existing app, or prepares a TestFlight, App Store or Google Play upload or submission, even if they only mention one piece such as screenshots, splash, permissions, AdMob, IAP, sign-in, push or a store rejection. Covers ASO and naming, mobile UI additions, motion and haptics, accessibility, onboarding, permission timing, ads consent order, IAP and subscriptions, review prompt, support, sign-in and account deletion, push, security, privacy manifest and Data safety, analytics, localization, testing, store screenshots, the Android 12+ splash, and backend checks.
---

# New app

Goal: an app that is unique, with great UI/UX, purposeful motion, secure, and only the features it needs, each one done right.

- Each topic uses the same parts: **Needed when**, **Not needed when**, **Do it right**, **Check**.
- `[invented]` marks a call with no source behind it; overrule it cheaply.
- A number from a past measurement is an observation, not a law: re-measure before building on it.
- "Owner" means the user who decides product direction and what ships.
- When a value is specific to this owner or this app (a URL, a size, an account id, a locale list) and is not known for certain, ask the user. Never guess one or derive it from a pattern.

## Owner decisions that bind every app

- An overhaul adds no new ad unit, no new IAP, and no Remove Ads. It keeps the existing monetization.
- The UMP consent message is already published in AdMob for every app. Only the in-app SDK call can be missing.
- Store copy is en-US only. Add en-GB, vi or any other locale only when the owner asks.
- iPhone screenshots use the size the app's earlier accepted set used; ask if unknown. Never 1320x2868 unless the owner says so: sets at that size were rejected.
- Play closed test: 12 testers opted in for 14 continuous days before production access. Not 20.
- Every rule is configurable from the first prototype.
- Batch fixes. Send build notes (Fixed, Changed, New) and build only after the owner's ok. Upload no build ahead of known queued fixes.
- Every report lists every known gap with its status (fixing, blocked, waiting, depends on).

## 1. Uniqueness and ASO before building

**Needed when:** always, before any project folder exists.

**Not needed when:** an overhaul of a live app whose name already ranks; touching the name risks lost rank [invented].

**Do it right:**
- Settle the name, in the form "X: Y" with at most 30 characters, plus a subtitle of at most 30 characters, before creating the project. Research ASO first; never create the project ahead of it.
- The ASO deliverable is a paste sheet: `ASO.md` holds only the store fields per language, each in its own code block. Research goes in a separate file, `research.md`.
- Search name collisions and trademarks before committing to a name, and write the result down. A collision routes other companies' support mail to you; a trademark may only surface through this search.
- Sweep for look-alikes as well as names. A colour scheme or layout that reads as a famous app (for example Wordle's green/yellow/grey) invites a takedown. Pick your own hues.
- The product must be more than a repackaged or widely available app [ARG 4.2, 4.3(b)].
- Re-check every claimed differentiator against current competitors; a "unique" feature is often standard.
- Apple indexes name, subtitle and keywords as one bag. The keyword field carries only words not already in the other two.
- No competitor names in metadata [ARG 2.3.7].
- Each locale has its own keyword index: plan keyword sets per storefront with no shared words. Apple ignores diacritics, so never spend characters on unaccented duplicates.
- Write store copy from the app's code and data files, never from memory. Never list a feature the build does not have.
- Ratings and download velocity drive rank. An app with zero ratings does not rank. Plan the review prompt from day one (`references/monetization.md`, review prompt).

**Check:** Are the name and subtitle each 30 characters or fewer and settled in `ASO.md` before the project folder was created, with a collision and trademark search written down?

## Which file to read

All under `references/` next to this file. Read the file before the work it covers.

| Work | File |
|---|---|
| Screens, layout, motion, haptics, accessibility, small screens, onboarding (mobile additions to `designing-interfaces`) | `references/design.md` |
| Permission prompts, ads (additions to `serving-mobile-ads`), IAP and subscriptions, review prompt | `references/monetization.md` |
| Support channel, sign-in, account deletion, push, security, backend data and performance | `references/accounts-backend.md` |
| Privacy manifest, Data safety, analytics, crash reporting, startup, localization | `references/privacy-analytics.md` |
| Testing, store screenshots, Android 12+ splash, store submission | `references/store.md` |
| Source URLs behind every `[tag]` | `references/sources.md` |

## Related skills

- UI: load `designing-interfaces` before any screen work. `references/design.md` adds only mobile rules on top of it.
- Ads: load `serving-mobile-ads` before any ad work. `references/monetization.md` adds only what it lacks.
- `asc-*` (App Store Connect), `gplay-*` (Google Play), `writing-copy` (store prose).
- `designing-interfaces`, `serving-mobile-ads` and `writing-copy` are project skills copied into each app repo's `.claude/skills/`. If one is missing in the current project, tell the user and ask where to take it from; do not apply its rules from memory.

## Pre-submit checklist

Copy this block into the response and tick each item. Any unticked item blocks the submission. "If" items apply only when the app has that feature.

```
Identity and store
- [ ] 1. Name and subtitle each 30 characters or fewer, copied from ASO.md
- [ ] 2. Store locales exactly the owner-approved set (en-US by default); metadata dry run shows zero deletes
- [ ] 3. iPhone screenshots at the app's earlier accepted size (asked if unknown); iPad and Play sets at their accepted sizes; at most 10 per size; no alpha
- [ ] 4. Screenshots, Play phone screenshots and feature graphic are marketing shots: real capture in a phone frame, one benefit headline in the store language, brand palette, hook first slide on a real figure or the core value, no price, "free" or "Premium" label
- [ ] 5. Every store asset (screenshots, previews, promo images) marked current against this build; nothing still rendering
- [ ] 6. App Store description ends with the app's privacy policy URL (confirmed, never guessed) and Apple's standard EULA line; Play description ends with the privacy line
- [ ] 7. Privacy URL returns 200; the page matches the App Privacy label and Data safety
- [ ] 8. Support URL returns 200 and shows a contact method
- [ ] 9. Grep of store text, captions and UI for third-party brand marks returns nothing; every person in a screenshot is AI-generated or covered by a signed release
- [ ] 10. Store copy lists only features the build has

Build
- [ ] 11. Grep for PLACEHOLDER|TODO|example.com|lorem|XXXX returns nothing in source and metadata
- [ ] 12. iOS deployment target at least 15.0 in the Podfile and all build configs; Android targetSdk at the current Play floor (read today); minSdk from the real plugin floor (at least 24)
- [ ] 13. Version name is new (not an approved, closed name), same on iOS and Android; encryption answer set
- [ ] 14. Podfile.lock present and unchanged except intended bumps
- [ ] 15. Every *UsageDescription in the default language, with InfoPlist.strings per extra locale
- [ ] 16. PrivacyInfo.xcprivacy in the archive; NSPrivacyTracking false or absent for an AdMob app
- [ ] 17. Release build free of strings in the wrong language (guard passes)
- [ ] 18. Android: cold-start first frame on an Android 12+ emulator shows the splash art whole inside the circle; adaptive icon foreground inside the 66% safe zone

Behaviour, on a fresh device
- [ ] 19. Cold launch with no network reaches the home screen within 8 s
- [ ] 20. No permission, rating or purchase requested before the first value moment; app works with every permission denied
- [ ] 21. If ads: serving-mobile-ads audit A to H passes; on a real device UMP shows a form (no code 4); the privacy options entry opens when required
- [ ] 22. If IAP: prices localized or Retry shown (never a dead button); restore only on the Restore row (iOS); refunds and expiry downgrade
- [ ] 23. If accounts: Sign in with Apple, in-app deletion, the Apple revoke and the Play web deletion link all work
- [ ] 24. If push: a server-sent push arrives on a real device and opens the right screen
- [ ] 25. Exactly one automatic review call behind an engagement gate; the Rate row opens the store URL
- [ ] 26. designing-interfaces verify pass is clean; at 375x667 and the largest Dynamic Type the primary action is visible with no clipped label; no control under the notch or banner
- [ ] 27. Motion budget test passes; Reduce Motion shows final frames with haptics still firing
- [ ] 28. Every displayed number matches the oracle script on a real-UI walkthrough of every flow; every screenshot looked at
- [ ] 29. A forced test crash is visible in the crash console with symbols

Backend (if any)
- [ ] 30. RLS on every exposed table; EXECUTE revoked from public, anon and authenticated on privileged functions; no secret key in the client
- [ ] 31. Rate limits stored in the database; rewards and purchases granted only from verified server callbacks
- [ ] 32. Both Supabase advisors (security, performance) report zero WARN (or the equivalent linter of the backend in use)
- [ ] 33. Realistic-volume scale test meets every read target with totals matching the oracle; monthly database cost estimated
- [ ] 34. Every external import refuses unknown rows alone, with a state table for every status and stuck-state alarms on the admin home
- [ ] 35. Migrations deployed before the code that needs them

Process
- [ ] 36. The report to the owner lists every known open gap with its status
- [ ] 37. Overhaul: zero new ad units and zero new IAP
- [ ] 38. Every queued fix done before the build is uploaded
- [ ] 39. Play: Data safety actually set and the app not left Unpublished after the last edit
```

If an item fails, fix it, then re-run that item and every item it can affect before ticking.
