# Consent, tracking, test ads, new ad units

## Contents
- Consent order (UMP)
- Tracking prompt (iOS)
- SDK start
- Test ads
- New apps and ad units

## Consent order (UMP)

Order on every launch, all before any load:

1. Request an update of the consent information on every launch. Google: "You should request an update of the user's consent information at every app launch." and "We don't recommend that you check consent status in another way" (cached or saved consent). Sources: https://developers.google.com/admob/ios/privacy, https://developers.google.com/admob/android/privacy, https://developers.google.com/admob/flutter/privacy.
2. Load and present the consent form if required (`loadAndPresentIfRequired` on iOS, `loadAndShowConsentFormIfRequired` on Android and Flutter). "If no privacy message forms require collection of user consent prior to requesting ads, the callback is invoked immediately." The form appears only for users the console message targets (for example the EEA and UK).
3. Check `canRequestAds`. Google: "Before requesting ads, use canRequestAds to check if you've obtained consent from the user." It "always returns false until you have called" the consent update.
4. Only when it is true may any trigger call `load()`.

Details Google states:
- Check `canRequestAds` both after gathering consent and right after the consent update, because "The UMP SDK might have obtained consent in the previous app session." Guard with a flag so the two checks do not cause redundant requests.
- "If an error occurs during the consent gathering process, check if you can request ads." The SDK uses the consent status from the previous session.

Design consequences:
- First launch can have zero requests by construction: conditional formats appear only after the consent steps ran, and App Open is off on first launch.
- When `canRequestAds` is false, do not render ad options; skip App Open with `reason: consent`. Declining consent or tracking must not change gameplay or core function.
- Do not request ads in a region that needs consent before the form has been answered.

## Tracking prompt (iOS)

- Google's IDFA page: the consent form can show an IDFA message first, and then the ATT alert. "Your app then shows an IDFA message before the ATT alert." Source: https://developers.google.com/admob/ios/privacy/idfa.
- Decide once: either the UMP IDFA message presents the ATT alert, or the app calls the tracking authorization API itself. Never both. Whether a separate direct call is also needed is not stated on the Google page; check the UMP SDK reference for your version.
- Field observation, not verified against Apple's documentation: the ATT alert may fail to appear if requested when the app is not in the active state. Request it from an active foreground screen, not from early launch code. Confirm on a real device and in Apple's documentation.
- With tracking denied, ads still load (non-personalized). Declining does not block loading.
- Order problem seen in practice: requesting ATT after the first loads already fired. Resolve consent and tracking before the first load.

## SDK start

- Google: before loading ads, start the Mobile Ads SDK (https://developers.google.com/admob/ios/quick-start). The Google UMP pages do not specify the ordering of SDK start relative to the consent flow; they require only that consent be checked before requesting ads. Request-specific consent flags, where used, must be set before initialization (same quick-start page).
- Practical rule: start the SDK on the path that has already passed the `canRequestAds` check. Do not block the UI on the start completion; the completion handler can be delayed while adapters finish, so run the rest of the app meanwhile.
- No load before the SDK start has been called.

## Test ads

Google: "It is important to use test ads during development so that you can click on them without charging Google advertisers." "If you click on too many ads without being in test mode, you risk your account being flagged for invalid activity." Sources: https://developers.google.com/admob/ios/test-ads, https://developers.google.com/admob/android/test-ads.

Rules:
- Debug builds use Google's demo ad units. Current demo unit ids are listed on the test ads pages above; copy them from there. Demo units are "not associated with your AdMob account, so there's no risk of your account generating invalid traffic."
- Selection is compile time (`#if DEBUG`, build config, `kDebugMode` or `__DEV__` compiled out of release). No runtime toggle, no stored preference, no environment read that could switch a shipped build to test ads or real ads.
- Never click real ads on your own devices. Register your devices as test devices instead: in the AdMob UI ("New test devices typically start serving test ads in your app within 15 minutes, but it can also take up to 24 hours") or in code (`testDeviceIdentifiers` on iOS, `RequestConfiguration.Builder.setTestDeviceIds()` on Android). "Be sure to remove the code that sets these test devices before you release your app." Use a compile-time list that is empty in store builds.
- A beta distribution (for example a TestFlight build) is a release build and serves real units. Register the testers' devices or use the compile-time list before anyone taps an ad.
- Illustration: one app shipped a runtime test-ads switch to see anything at all and removed it minutes later. A switch that can reach production is a risk even when it is off.
- Mediated ads show no test label; "You are responsible for ensuring that test ads are enabled for each of your mediation networks" (Android test ads page).

## New apps and ad units

- A new ad unit needs time: "If testing new ad units, wait about 2 hours for them to become active." Source: https://support.google.com/admob/answer/15090849.
- Low match rate "can occur for up to one week after a new app or ad unit is created." Source: https://support.google.com/admob/answer/9655701.
- For no-fill generally: "there may not have been advertising demand available at the time of your request"; advertisers can target regions, platforms and user profiles, which limits availability (https://support.google.com/admob/answer/15090849).
- Consequence for code: a new app or unit returns many no-fills. A retry loop with no cap (observed once on a banner, hundreds of requests at about 3% match) only inflates request counts. Cap retries and expect low match until the app and units are active.
