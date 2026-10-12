# App Open ads

## Contents
- What Google says
- Show conditions
- Load moments
- Cold start
- Retry
- Audit hits

## What Google says

- Expiry: four hours (https://developers.google.com/admob/ios/app-open, https://developers.google.com/admob/android/app-open, https://developers.google.com/admob/flutter/app-open).
- "Your ad should show quickly, so it's best to load your ad before you need to display it." (iOS and Android pages)
- "Wait to show your first app open ad until after your users have used your app a few times." (iOS page; Android and Flutter pages say the same)
- "Show app open ads during times when your users would otherwise be waiting for your app to load." (iOS page)
- Cold start: "The preferred way to use app open ads on cold starts is to use a loading screen to load your game or app assets." "If your app has completed loading and has sent the user to the main content of your app, don't show the ad." (iOS and Android pages)
- "request the next app open ad once the first one finishes presenting" (iOS page); the sample reloads in the dismiss callback. The Android sample leaves the reload as a comment, so add the call yourself (https://developers.google.com/admob/android/app-open).
- Load assets in a background thread while the ad is displayed (Android and Flutter pages).

## Show conditions

Evaluate in this order; the first failing check logs `app_open_skipped {reason}` and stops:

1. Not the first launch ever (Google: wait until users have used the app a few times; a stricter "second launch onward" is a practitioner default).
2. `canRequestAds` is true.
3. No full-screen ad is presenting.
4. The trigger is a cold start, or a foreground return after a minimum time in the background. Starting value: 30 minutes (practitioner default).
5. A minimum time since the last App Open ad was shown. Starting value: 30 minutes. Persist the last shown time.

When all pass:
- A valid held ad exists: show it now, before the content is interactive.
- No valid ad: skip silently, let the app start, make sure a load is in flight for next time. No wait screen and no timer holding the user, except the cold start case below.
- On show: set `isPresentingFullScreenAd`, record the shown time, log `ad_shown` from the impression callback.
- On dismiss or failed-to-show: clear `isPresentingFullScreenAd`, release the ad, then load so the next qualifying foreground has one.

Define "session" as one foreground stretch: a return after the minimum background time is a new session, so "once per session" and "not twice within 30 minutes" agree.

## Load moments

Load, through the guard, at these moments and no others:

1. Cold start after consent is resolved, when this is not the first launch ever.
2. After a shown ad is dismissed or fails to present.
3. On a qualifying foreground where no valid ad was held.
4. On a foreground where the held ad has expired.
5. Optional, practitioner judgment: when the app enters the background with nothing held and nothing in flight. The OS gives a short background window; if the request does not finish, the callback lands on the next foreground and the ad is held from then. Verify on device before relying on it.

Not load moments: a timer, a foreground return under the minimum background time (this includes returning from an ad click-through), and the close of a rewarded ad.

Expected shape: about one request per shown ad plus one per expiry. A load that arrives after the trigger that asked for it is not wasted: it is held up to the lifetime and shown on the next qualifying return.

## Cold start

An App Open ad does not survive a killed app, so on a cold start nothing is held. Two valid designs:

- **Never wait** (default): skip on cold start if nothing is held; load for next time.
- **Splash wait**: from the second launch onward, hold the loading screen for a short bounded time (starting value: 3 seconds, practitioner default) while the ad loads. If it arrives, show it over the loading screen; if not, continue and make no retry for that launch.

Google's guidance supports showing only from a loading screen. Never show once the user has reached the main content. Choose one design and write it down; do not mix.

## Retry

Use the ladder in [loading-and-expiry.md](loading-and-expiry.md), capped, stopping on verified no-fill, restarted by each load moment above. Do not add a long backoff memo: a no-fill costs about one request per launch or return, and a multi-hour memo starves the format where fill is intermittent.

## Audit hits

- App Open loaded at launch before consent.
- No `loadedAt` check before show (expired ad shown or silently invalid).
- Ad shown after the user already reached main content on a cold start.
- Ad shown on the first launch ever, or twice within a short window.
- No reload after dismiss.
- A foreground observer that loads on every foreground with no condition.
