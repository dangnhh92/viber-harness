# Loading, expiry, retry

## Contents
- Loader state
- The load guard
- Expiry
- Retry ladder
- Classifying errors
- Google-managed preloading
- Common failure patterns

## Loader state

One state object per format (App Open, Rewarded, Interstitial). Keep it in memory; persist only what must survive a cold start (for example the time an App Open ad was last shown).

```
ad:             the held ad object, or null
loadedAt:       timestamp of the successful load
isLoading:      bool
loadStartedAt:  timestamp
retryStep:      int
retryTimer:     one-shot timer, or null
```

Shared across formats: `isPresentingFullScreenAd`, `canRequestAds`, `sessionRequests`.

## The load guard

Every load path goes through one function. Pseudocode, any language:

```
load(format, reason):
  if ad != null and notExpired(ad):  return        // reuse, never replace a valid ad
  if isLoading:                      return        // one in flight
  if !canRequestAds:                 return        // consent not resolved
  if offline:                        return        // see below
  if sessionRequests >= ceiling:     return        // bug guard
  isLoading = true; loadStartedAt = now; sessionRequests += 1
  request(
    onLoaded: ad = x; loadedAt = now; isLoading = false; retryStep = 0
    onFailed(err): isLoading = false;
                   if isNoFill(err): stop chain, log
                   else: scheduleRetry(retryStep)
  )
```

Rules:
- Clear `isLoading` in both callbacks and by a stale timeout in case the SDK never calls back. Starting value: 30 seconds (practitioner default, not a Google figure).
- Offline: skip the request when the platform reports no connectivity. Treat unknown status as online: reachability monitors give false negatives, and a wrongly skipped load costs revenue while a wrongly sent one costs one request. Coming back online does not trigger a load; the next intent does.
- Two placements that use one ad unit share one holder and one `load()`. Never two parallel loads for the same unit.
- Session ceiling: a per-session cap on total requests across formats. Starting value: 30. It is a guard against a bug in the load conditions, not a policy; at the expected one to three requests per session it should never fire. Log when it does.

## Expiry

Platform facts:
- App Open: "App open ads will time out after four hours. Ads rendered more than four hours after request time will no longer be valid and may not earn revenue." Source: https://developers.google.com/admob/ios/app-open (the Android page https://developers.google.com/admob/android/app-open and the Flutter page https://developers.google.com/admob/flutter/app-open state the same four hours).
- Rewarded: "Because ads expire after an hour, you should clear this cache and reload with new ads every hour." Sources: https://developers.google.com/admob/ios/rewarded and https://developers.google.com/admob/android/rewarded.
- Interstitial: same one hour statement. Source: https://developers.google.com/admob/ios/interstitial.

Practice:
- Store `loadedAt` with the held ad. Before every show, check `now - loadedAt` against the lifetime. Google's App Open pages show this check (a load timestamp compared with the current time).
- Use a lifetime slightly under Google's: for example 3 hours 55 minutes and 55 minutes (practitioner margins).
- A held ad is reused. A rewarded ad loaded for one screen is shown on a later screen if the first offer was declined.
- Never discard a valid ad to load a fresher one. Illustration: one app used a 120 second staleness window for a rewarded ad that stays valid for about an hour, so it threw away good fills and re-requested. The window that decides when to ask again and the window that decides how long an answer is good are different numbers.
- On expiry: set the ad to null, log `ad_expired`, reload only if the format's load condition still holds.
- A shown ad is single use. Release it in the dismiss and failed-to-show callbacks (iOS `adDidDismissFullScreenContent`, Android `onAdDismissedFullScreenContent`; Flutter also calls `dispose()` there). Source: https://developers.google.com/admob/android/rewarded and https://developers.google.com/admob/flutter/rewarded.
- Near expiry: when a held ad has little lifetime left (starting value: under 5 minutes) and a load condition currently holds, a fresh load avoids offering an ad about to expire. If no condition holds, let it expire.

## Retry ladder

Never a periodic timer. A bare clock retries an empty slot forever, including in states where nobody needs the ad.

Ladder (practitioner starting values): 5 s, 15 s, 45 s, 2 min, 5 min, then stop. At most six requests per chain. Google's preloading page confirms exponential backoff as a pattern (https://developers.google.com/admob/ios/ad-preloading) but gives no values.

Rules:
- A chain runs only while the format's load condition still holds. When the condition ends (screen left, app backgrounded), cancel the timer and reset the step. A retry with nobody close to needing the ad is the periodic-timer bug in disguise.
- A new intent restarts a stopped chain from step 1.
- A verified no-fill stops the chain at once. Do not climb the ladder against a server that just said no. No cross-session memo and no multi-hour backoff: the next intent re-probes with one request.
- Any other error (network, timeout, unknown): next rung.
- A fill resets the step.
- One immediate reload is allowed after a failed show, because the user is waiting.

Illustration: an app portfolio that retried every empty rewarded slot on a 30 second timer saw its rewarded match rate in one region fall from near 100% to about 5%, with thousands of doomed requests and almost no impressions. Several other apps in the same portfolio still ran a flat 60 second retry with no cap and no error branch.

## Classifying errors

A no-fill is a successful request with no inventory. It is not a connectivity problem and not a code bug.

Compare against the platform's named constant, never a literal number shared across platforms. The numbers differ:

| Platform | No-fill | Network | Source |
|---|---|---|---|
| iOS `GADErrorCode` | `noFill` = 1 | `networkError` = 2 | https://developers.google.com/admob/ios/api/reference/Enums/GADErrorCode |
| iOS server failure | `serverError` = 3 | | same page |
| iOS timeout | `timeout` = 5 | | same page |
| Android `AdRequest` | `ERROR_CODE_NO_FILL` = 3 | `ERROR_CODE_NETWORK_ERROR` = 2 | https://developers.google.com/android/reference/com/google/android/gms/ads/AdRequest |

Code 3 is no-fill on Android and a server error on iOS. A shared cross-platform literal is a bug.

Flutter and React Native: wrappers forward native codes, but this skill did not verify how each wrapper exposes them. Needs confirming against the wrapper's own docs before comparing numbers; prefer the wrapper's named constants if it has them.

Unrecognised errors keep retrying on the ladder. Only a verified no-fill stops a chain.

## Google-managed preloading

Google offers a managed preloading feature. Facts from the docs:
- Formats (iOS page): interstitial, rewarded, rewarded interstitial, app open. Android page: interstitial, rewarded, app open.
- "automatically preloads the next ad in the background" after an ad is retrieved; "automatically retries failed requests using exponential backoff"; "automatically refreshes ads before they expire (typically after one hour)."
- "We recommend keeping a buffer size of two for each preload ID." Default limit: a maximum of 6 preloaded ads in memory.
- Start: "When the app starts, call the `preload` method once" (iOS); Android: "call the `start` method once." Stop per preload ID or all.
- Page titles mark it beta; check the current status on the page before adopting.
Sources: https://developers.google.com/admob/ios/ad-preloading and https://developers.google.com/admob/android/ad-preloading.

Trade-off (judgment, not a Google claim): the feature refills and retries on its own, so it keeps a warm ad and a request stream whether or not a show is plausible. For formats shown on most sessions (App Open, an interstitial at a frequent trigger) that is fine. For conditional rewarded placements it recreates the launch-preload waste. If used there, start the preloader at intent and stop it when intent ends. Whether starting a preloader later than app start is supported is not stated on the pages above; needs confirming.

## Common failure patterns

- Preload at init for a placement most sessions never reach.
- Lazy loader with no caller after a preload was removed (feature dies silently).
- First load fired before the SDK start or before consent resolved.
- Retry timer that survives the screen that needed the ad.
- Two loaders for one ad unit.
- Treating every error as retryable, including no-fill.
