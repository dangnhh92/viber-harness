---
name: serving-mobile-ads
description: Guides implementing and auditing AdMob (Google Mobile Ads) ad loading in iOS and Android apps built with Swift, Kotlin, Flutter or React Native. Covers when to load App Open and Rewarded ads (on intent, not at launch), expiry, retry and backoff, no-fill handling, UMP consent ordering, test ads, and measuring match rate and show rate. Use when writing or reviewing code that loads or shows ads, when ad requests are high but impressions are low, when match rate or show rate looks wrong, or when asked for an ad loading audit.
---

# Serving mobile ads

Goal: every ad the app loads has a realistic chance of being shown, and every moment a user could see an ad has one ready. Two failure directions, measured separately:

- **Waste**: ads loaded and never shown (low show rate, inflated request count).
- **Starvation**: a moment where an ad could have been shown and none was ready.

Fixing one can cause the other. Always check both (see [references/measurement.md](references/measurement.md)).

## Vocabulary (used the same way in every file)

| Term | Meaning |
|---|---|
| load | one ad request to the SDK for one ad unit |
| hold | keep a loaded, unused ad object in memory |
| show | present a held ad |
| intent | a signal that the user is close to a moment where an ad would be shown |
| load condition | the app-state test that says intent is present now |
| match rate | matched requests / ad requests (did AdMob return an ad) |
| show rate | impressions / matched requests (did the app use what it got) |
| no-fill | the request succeeded but no ad was returned |

Definitions of match rate and show rate: https://developers.google.com/admob/api/v1/report-metrics-dimensions

## Core rules

1. **Load on intent, not at launch.** For a format that is shown only on some paths (rewarded, conditional interstitial), load when a load condition becomes true, and keep the ad ready until the moment of need. Moving the load closer to the show is the cure; removing the load is not. Illustration: an app portfolio measured about a 3% rewarded show rate when ads were loaded at launch. After moving loads to intent, requests fell by roughly 90% while impressions held or rose. Details: [references/rewarded.md](references/rewarded.md).
2. **One load in flight per format, none while a valid ad is held.** Guard with a flag cleared on success, failure and a stale timeout. Details: [references/loading-and-expiry.md](references/loading-and-expiry.md).
3. **Track expiry per held ad.** App Open ads expire after four hours; rewarded and interstitial ads after an hour (Google docs, cited in the reference). Do not confuse "how often to ask" with "how long an answer is good": never discard a valid ad to load a fresher one.
4. **Retry on a ladder with a cap, never on a bare periodic timer.** A flat timer in a region or state with no demand turns one no-fill into hundreds of requests. Stop on verified no-fill; restart on the next intent. Details: [references/loading-and-expiry.md](references/loading-and-expiry.md).
5. **A no-fill is not a network error.** Classify errors by the platform's named constants. The numeric codes differ per platform.
6. **No request before consent is resolved.** Order: consent info update, consent form if required, check `canRequestAds`, then load. Details: [references/consent-and-testing.md](references/consent-and-testing.md).
7. **Never a real ad unit in a debug build, never a runtime test switch in a release build.** Details: [references/consent-and-testing.md](references/consent-and-testing.md).
8. **Never fail silently on a user-initiated ad.** If the user tapped for an ad and none is ready, show a state (loading, unavailable), not nothing.
9. **Log impressions only from the SDK impression callback, and grant rewards only from the earned-reward callback.**
10. **Every load path has a caller and a test.** Removing a preload can silently kill a feature whose lazy loader nobody calls.

## Implement workflow

Copy this checklist and track progress:

```
Implementation:
- [ ] 1. List every place an ad can be shown (placement) and its format
- [ ] 2. For each placement, write its load condition in one sentence (never "app start" for conditional formats)
- [ ] 3. Build one loader per format with the guard, expiry check and retry ladder (loading-and-expiry.md)
- [ ] 4. Wire consent first, then the SDK start, then triggers (consent-and-testing.md)
- [ ] 5. Add format specifics (app-open.md, rewarded.md, interstitial-and-banner.md)
- [ ] 6. Add the events from measurement.md before shipping, not after
- [ ] 7. Test with Google's test units; run the audit checklist below on the finished code
```

Step 2 is the decision that matters most. If the sentence for a placement cannot be written without "when the app opens", ask whether the placement is shown on most sessions. If not, it is a conditional format and must not preload at launch.

## Audit workflow

Read the ad module first, then grep the whole project. Report evidence (file and line), not impressions.

```
Audit:
- [ ] A. Inventory: every load call, every show call, every timer in the ad code
- [ ] B. Load triggers
- [ ] C. Guards and expiry
- [ ] D. Retry
- [ ] E. Consent and init order
- [ ] F. Test ads and ids
- [ ] G. Show path and callbacks
- [ ] H. Measurement
```

**A. Inventory.** Useful greps (adapt to the framework): `load(`, `RewardedAd`, `AppOpenAd`, `InterstitialAd`, `Timer`, `periodic`, `setInterval`, `setTimeout`, `asyncAfter`, `Future.delayed`, `didBecomeActive`, `onResume`, `initState`, `useEffect`, `viewDidLoad`, `onCreate`.

**B. Load triggers.**
- [ ] No conditional-format load at app start, screen mount, level start, on dismiss of an unrelated ad, or on reconnect.
- [ ] Each load has a stated load condition that is true only when the user is plausibly close to a show.
- [ ] Every load path has at least one caller.

**C. Guards and expiry.**
- [ ] A load returns at once when a load is in flight or a valid ad is held.
- [ ] The in-flight flag clears on success, failure and a stale timeout.
- [ ] Each held ad stores a load timestamp and is checked before every show.
- [ ] A shown ad is released (set to null, disposed where the framework requires it) in the dismiss and failed-to-show callbacks.
- [ ] A valid held ad is reused across screens instead of discarded.

**D. Retry.**
- [ ] No periodic timer re-requests an empty slot.
- [ ] Retries use a capped ladder and stop at the end.
- [ ] A verified no-fill stops the chain; other errors move to the next rung.
- [ ] The chain is cancelled when the load condition ends.
- [ ] A per-session request ceiling exists as a bug guard.

**E. Consent and init.**
- [ ] The consent info update runs on every launch.
- [ ] No load is reachable before `canRequestAds` is true.
- [ ] If the SDK is started, it is started on a path that already passed the consent check.
- [ ] iOS: exactly one component presents the tracking prompt (UMP IDFA message or a direct call, not both).

**F. Test ads and ids.**
- [ ] Debug builds use Google's test units; release builds use real units; the choice is compile time.
- [ ] No runtime toggle, stored flag or env read that switches to test ads in a shipped build.
- [ ] Test device ids set in code are removed or empty in store builds.

**G. Show path and callbacks.**
- [ ] The reward is granted in the earned-reward callback, not on dismiss.
- [ ] The impression is logged in the impression callback, not before the show call.
- [ ] A user-initiated ad with nothing ready shows a state, not silence.
- [ ] No ad shows over a presenting ad, and no ad interrupts a task in progress.

**H. Measurement.**
- [ ] Events cover requested, filled, failed (with code and a no-fill flag), skipped (with reason), shown, expired.
- [ ] Both waste (show rate) and starvation are computable from the events.

**Report format.** For each failed item give: item letter, what the code does, file and line, which core rule it breaks, and the smallest fix. End with the open items and what could not be verified (for example a flow reachable only on a physical device).

## Format notes

| Format | Load when | Expires after | Reload after show | Reference |
|---|---|---|---|---|
| App Open | cold start after consent (not first launch ever), after a shown ad, when a held ad is missing or expired | 4 hours | yes | [references/app-open.md](references/app-open.md) |
| Rewarded | a load condition (user near need) becomes true | 1 hour | only if the load condition holds again | [references/rewarded.md](references/rewarded.md) |
| Interstitial | trigger fires often: preload and reload after dismiss; rare trigger: on intent | 1 hour | yes if the trigger is frequent | [references/interstitial-and-banner.md](references/interstitial-and-banner.md) |
| Banner | on screen display, with a capped retry | not applicable | not applicable | [references/interstitial-and-banner.md](references/interstitial-and-banner.md) |

Expiry sources: https://developers.google.com/admob/ios/app-open, https://developers.google.com/admob/ios/rewarded, https://developers.google.com/admob/ios/interstitial

## Framework notes

The rules are SDK-level and identical across Swift, Kotlin, Flutter and React Native. Callback names differ (for example `adDidDismissFullScreenContent` on iOS, `onAdDismissedFullScreenContent` on Android and Flutter). Flutter ad objects must be disposed when no longer needed. React Native wrappers are third-party; confirm in the wrapper's own documentation that error codes and callbacks map to the native ones before relying on a code comparison. Map names in [references/sources.md](references/sources.md).

## Honesty about values

Google's documents state the expiry times, the consent ordering and the preloading behavior. Every other number in this skill (ladder steps, caps, timeouts, targets) is a practitioner starting value, labelled as such. Tune them against measured show rate and starvation; do not present them as Google figures.

## References

- [references/loading-and-expiry.md](references/loading-and-expiry.md): loader state, guard, expiry, retry ladder, no-fill classification, Google-managed preloading.
- [references/app-open.md](references/app-open.md): App Open load and show rules.
- [references/rewarded.md](references/rewarded.md): intent loading, button states, reward timing.
- [references/consent-and-testing.md](references/consent-and-testing.md): UMP order, tracking prompt, test units, new ad units.
- [references/measurement.md](references/measurement.md): metrics, events, reading the pair, targets.
- [references/interstitial-and-banner.md](references/interstitial-and-banner.md): generalizable lessons for the other formats.
- [references/sources.md](references/sources.md): every Google and Anthropic URL used, with what it supports.
