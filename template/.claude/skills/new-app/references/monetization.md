# Permissions, ads, IAP, review prompt

## Contents
- Permission timing
- Ads (UMP, ATT order, placements): additions to `serving-mobile-ads`
- IAP and subscriptions
- Review prompt

## Permission timing (notifications, ATT, camera, photos, location)

**Needed when:** a feature truly needs the resource [HIG-privacy].

**Not needed when:**
- A system picker does the job without a permission [invented, verify per API].
- Never request at launch unless the app cannot function without it [HIG-privacy].

**Do it right:**
- Ask at the moment the feature is used, after the first value moment (for example push after the first completed core action) [HIG-privacy].
- Android: wait for an action such as tapping an alert bell, a follow, or the third or fourth launch [And-notif].
- A pre-prompt screen may precede the system alert [HIG-privacy]:
  - Exactly one button, labelled "Continue" or "Next", never "Allow".
  - No close or cancel.
  - Never an incentive, never an image of the alert.
- A "Later" in a pre-prompt re-asks at most once; a stray tap must not use up an ask.
- Read `canAskAgain` (Expo) or `shouldShowRequestPermissionRationale` (Android). Render "not asked", "denied" and "off in Settings" as distinct states; when the system will no longer prompt, offer "Open Settings".
- Android 13+: declare and request `POST_NOTIFICATIONS` at runtime [And-notif].
- Purpose strings: one brief, specific sentence in sentence case with a period. Never "This app needs access" [HIG-privacy].
- Every `*UsageDescription` is in the app's default language, with `InfoPlist.strings` per extra locale. A string in another language gets rejected under Guideline 4. `grep UsageDescription Info.plist` before every submit.
- The app keeps working when any permission is denied. Apple rejects apps that require push, location or tracking to function [ARG 5.1.2].
- ATT: order and single-path rule in `serving-mobile-ads`. AdMob never shows ATT for you; declaring tracking with no prompt in the app holds the review.

**Check:** Does `grep -i UsageDescription` show only default-language strings, and is no permission requested before the first value moment (verified on a fresh install)?

## Ads (UMP, ATT order, placements)

Ads: load `serving-mobile-ads` first. It owns:
- load on intent, one request in flight, ad lifetimes and reuse;
- the retry ladder, no-fill codes, the per-session cap, no periodic timer;
- the UMP, ATT and `MobileAds.start` order, `canRequestAds`, zero first-launch requests, the single ATT path;
- App Open rules and skip-reason logging;
- the earn callback and impression counting;
- test units, test devices and TestFlight serving real ads;
- measurement windows and show-rate, starvation and match-rate targets;
- its audit A to H (the grep checks).

This section holds only what it does not state.

**Needed when:** the app is free and its monetization is ads. Rewarded earns the most per show (one past measurement: about 4x interstitial and 35x banner eCPM; re-measure). In low-purchase markets prefer rewarded ads over IAP.

**Not needed when:**
- An overhaul: never add an ad unit.
- A subscription app where ads would undercut the paywall [invented].

**Do it right:**
- The language picker comes before consent on first launch, so UMP and ATT show in the chosen language.
- Call ATT about 250 ms after the scene becomes active; an immediate call can be dropped.
- A brand-new AdMob app has no consent message until one is published; UMP then fails with code 4 and the app makes zero requests. The simulator hides this: test on a device.
- Show a privacy options entry when `privacyOptionsRequirementStatus == .required`; it calls `presentPrivacyOptionsForm` (iOS) / `showPrivacyOptionsForm` (Android) [UMP-iOS; UMP-And].
- Await dismissal before continuing: `show()` returns when the ad is presented, not when it closes.
- Server-granted rewards come only from the AdMob SSV callback, with a non-empty `ssv_query` verified in production.
- iOS plist: `GADApplicationIdentifier`, `SKAdNetworkItems`, `NSUserTrackingUsageDescription`. Android manifest: `APPLICATION_ID`.
- A start that failed because the device was offline or consent was pending must be restartable.

**Check:**
- Does the `serving-mobile-ads` audit A to H pass?
- On a real device with a new AdMob app, does UMP show a form (no code 4)?
- When consent requires it, does a privacy options entry open the form?

## IAP and subscriptions

**Needed when:** the app unlocks features or content for money; Apple requires IAP for that [ARG 3.1.1]. Put the paywall where intent is highest; buyers often buy before trying anything.

**Not needed when:**
- Overhauls: no new IAP, no Remove Ads.
- Low-purchase markets: prefer rewarded ads.

**Do it right:**
- Before asking someone to subscribe, describe what they get for the price. Period at least 7 days [ARG 3.1.2(a), 3.1.2(c)].
- Subscription apps have working in-app Privacy and Terms links.
- Restore:
  - iOS: only from a Restore row, never at launch (it can pop an Apple ID prompt during review).
  - Android: restore silently at launch.
- On launch, re-derive entitlement from `currentEntitlements` (StoreKit 2) or past purchases; downgrade when it is gone. A cancelled subscriber must not keep Premium.
- Grants are idempotent, from one source. `approved` fires again on every launch and restore.
- Server validation: a status-0 receipt proves the receipt is genuine, not that it belongs to this app or user. Check `bundle_id`; make the original transaction id unique per account.
- Accept sandbox receipts in production; App Review buys with sandbox.
- Handle refunds: App Store Server Notifications on iOS, voided purchases on Android.
- Buy buttons stay disabled until the store's localized price loads; show Retry when products fail to load. A paywall with no products and dead buttons is rejected under 2.1(a)/(b).
- Cache a successful `isAvailable()` result, never a failed one.
- Remove Ads gates every banner, interstitial and App Open and removes the visible banner at purchase. Rewarded stays available.
- A new subscription is attached to a version, with a review screenshot, or it never ships. Check no product is left in READY_TO_SUBMIT.
- Each IAP gets its own promo image; one image reused across products is rejected under 2.3.2.

**Check:**
- On a fresh simulator (`xcrun simctl erase`), does the paywall show localized prices or a Retry, never a dead button?
- Does restore work from the Restore row only (iOS)?
- Does a refunded or expired purchase downgrade?

## Review prompt

**Needed when:** every public app. Ratings drive rank.

**Not needed when:** never omitted, but never on first launch or during onboarding [HIG-ratings].

**Do it right:**
- Ask after demonstrated engagement, at a natural break, after a happy moment: for example the first core outcome confirmed by the server, or after N clean uses, once per app version [HIG-ratings].
- System prompt only: `requestReview` (StoreKit), Play `launchReviewFlow`.
- Apple shows it at most 3 times in 365 days [SK-review]. Space your own asks (for example a 90-day throttle on a trusted clock; HIG says at least a week or two).
- Never call it from a button. The manual "Rate" row opens the store page: `https://apps.apple.com/app/id<ID>?action=write-review` on iOS (an explicit app id is required), the Play listing on Android.
- No question before the prompt ("Do you like the app?"), nothing overlaid on the Play card [Play-review]. Never gate a feature on a rating [ARG 3.2.2(x)].
- Expo: check `isAvailableAsync`, never `hasAction` (it opens the store mid-flow when only a URL exists).
- Lazy-import the native module so an OTA update reaching an older binary cannot crash.
- The prompt never appears in TestFlight; test it in a development build.

**Check:** Does `grep requestReview` hit exactly one automatic call site behind an engagement gate, and does the Rate row open the store URL?
