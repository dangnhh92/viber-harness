# Rewarded ads

## Contents
- Why not at launch
- Defining the load condition
- Holding and reuse
- Button states
- Showing and rewarding
- After the ad
- Audit hits

## Why not at launch

Google's pages show loading early as the sample pattern ("usually done in the `onCreate` method of an `Activity`", "build up a cache of preloaded ads", https://developers.google.com/admob/android/rewarded; "loading an ad inside the `GADInitializationCompletionHandler`", https://developers.google.com/admob/ios/rewarded). That is a convenient sample, not an efficiency recommendation, and for conditional placements it is the single largest source of waste seen in practice.

Illustration (anonymised aggregate): across a portfolio of apps over several months, rewarded ads were matched about 28,000 times and shown under 900 times, a show rate near 3%. The causes found in code were always the same: preload at launch for a placement most sessions never reach, plus a reload after every show. An app that moved the load to intent kept the same impressions with about 90% fewer requests. An app that only capped retries without moving the load saw its show rate keep falling: capping retries does not fix show rate.

The cure is moving the load closer to the show. An ad must still be ready at the moment of need.

## Defining the load condition

For each rewarded placement write the load condition: a signal that the user is close to needing the reward, true only on paths that plausibly lead to a show. None of these is a load condition: app start, screen mount, level start, a timer, a dismiss, a reconnect.

Examples of intent signals (adapt to the app):
- A resource the reward replenishes is nearly spent (starting value: a threshold chosen by judgment, then tuned with measurement; one app used "balance at 5 or below", another "moves left at 2 or below").
- A screen that offers the reward has opened and nothing is held (the on-demand fallback; it should be rare once the earlier signals work).
- The user opened a flow whose usual next step is the offer.

Tune the threshold with the pair of metrics in [measurement.md](measurement.md): too early shows as low show rate with low starvation, too late as high starvation with a healthy match rate.

Fallback path: if the offer opens and nothing is held or in flight, load then and show the loading state below.

## Holding and reuse

- One holder per ad unit, shared by every placement that uses the unit.
- A held ad survives screen changes. Load at intent on one screen, the user declines, show it on a later screen.
- Drop it only when shown, on expiry (one hour, https://developers.google.com/admob/android/rewarded), or on a failed show.
- Near expiry with a load condition currently true: refresh, so the offer is not made with an ad about to expire.
- Do not discard a valid ad to load a fresher one.

## Button states

Never show a button that plays nothing. Drive the control from loader state:

| Condition | Control |
|---|---|
| Valid ad held | enabled, normal label |
| Load in flight, within a short wait (starting value: 8 seconds) | disabled with a spinner; becomes enabled the instant the fill callback lands |
| Failed, ladder exhausted, or wait elapsed with no ad | disabled with an "unavailable, try later" message |
| Offline | disabled with an offline message |
| `canRequestAds` false | do not render the ad option; keep the non-ad path |

The non-ad path (close, restart, spend currency) stays enabled in every state. Log `rewarded_offer_shown {reason, ready: true|false}` when the offer opens so starvation is measurable.

Illustration: one app's rewarded button did nothing on no-fill until a toast was added; another disabled the button with an "ad not ready" label, which is the safer baseline.

## Showing and rewarding

- Grant the reward in the earned-reward callback (iOS `userDidEarnRewardHandler`, Android `onUserEarnedReward`, Flutter `onUserEarnedReward`). Google: "For Google ads, all `userDidEarnRewardHandler` calls occur before `adDidDismissFullScreenContent:`" and for mediated ads "the third-party ad source determines the callback order" (https://developers.google.com/admob/ios/rewarded, https://developers.google.com/admob/android/rewarded). Granting on dismiss risks double or missing grants; the earned callback is the contract.
- Log the impression in the SDK impression callback (`adDidRecordImpression` / `onAdImpression`), never before calling show. Logging before the show makes the app's own numbers lie.
- If the ad is dismissed without the reward callback firing, tell the user no reward was given and do not reload.
- Re-enable the UI and close the offer in the dismiss callback.
- On failed-to-show: release the ad, move the control to the failed state, log `ad_show_failed {format, code}`. One immediate reload is allowed because the user is waiting.

## After the ad

Release the ad (set to null; Flutter: `dispose()`; https://developers.google.com/admob/flutter/rewarded). Reload only when a load condition holds again, which on the same screen is usually not the case (the cap or the need is already spent). Do not reload on dismiss by default.

## Audit hits

- `load` call in app start, `viewDidLoad`, `initState`, `onCreate`, a mount effect, or an init-complete handler for a conditional placement.
- A reload in the dismiss callback with no condition check.
- Two placements that each own a loader for the same unit.
- A button that stays enabled with nothing held.
- Reward granted in dismiss.
- Impression logged before the show call.
- A lazy loader (`ensureLoaded`) with no caller.
