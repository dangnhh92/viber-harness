# Sources

Every platform fact in this skill comes from one of these pages. Re-read the page before relying on a number: documentation changes.

## Contents
- Google, ad formats
- Google, consent and testing
- Google, errors and metrics
- Callback name map
- Anthropic authoring guidance applied

## Google, ad formats

| URL | Supports |
|---|---|
| https://developers.google.com/admob/ios/app-open | App Open four hour expiry; best practices; cold start via loading screen; reload after dismiss; freshness check |
| https://developers.google.com/admob/android/app-open | same on Android; sample leaves the reload to the developer; background thread for assets |
| https://developers.google.com/admob/flutter/app-open | same on Flutter; timestamp check on the manager; dispose in dismiss and failed handlers |
| https://developers.google.com/admob/ios/rewarded | one hour expiry; reward handler fires before dismiss for Google ads; callback list |
| https://developers.google.com/admob/android/rewarded | one hour expiry; `onUserEarnedReward` before dismiss; release the ad in dismiss and failed-to-show |
| https://developers.google.com/admob/flutter/rewarded | a rewarded ad shows once; dispose in dismiss and failed-to-show; the page states no expiry period |
| https://developers.google.com/admob/ios/interstitial | one hour expiry; natural pauses; frequency; reload after dismiss |
| https://developers.google.com/admob/ios/ad-preloading | managed preloading: formats, auto refill, exponential backoff, buffer size, limit of 6, expiry refresh |
| https://developers.google.com/admob/android/ad-preloading | same on Android |

## Google, consent and testing

| URL | Supports |
|---|---|
| https://developers.google.com/admob/ios/privacy | consent update every launch; `canRequestAds` semantics; redundant request guard |
| https://developers.google.com/admob/android/privacy | same on Android |
| https://developers.google.com/admob/flutter/privacy | same on Flutter |
| https://developers.google.com/admob/ios/privacy/idfa | IDFA message before the ATT alert |
| https://developers.google.com/admob/ios/quick-start | start the SDK before loading ads; consent flags before initialization |
| https://developers.google.com/admob/ios/test-ads | test ads; invalid activity risk; test device registration; remove before release |
| https://developers.google.com/admob/android/test-ads | same on Android; 15 minute to 24 hour test device delay; mediation test ads |
| https://support.google.com/admob/answer/15090849 | new ad units about 2 hours; no-fill causes |
| https://support.google.com/admob/answer/9655701 | common causes of low match rate; up to one week for new apps or units |

## Google, errors and metrics

| URL | Supports |
|---|---|
| https://developers.google.com/admob/ios/api/reference/Enums/GADErrorCode | iOS codes: noFill 1, networkError 2, serverError 3, timeout 5 |
| https://developers.google.com/android/reference/com/google/android/gms/ads/AdRequest | Android codes: NO_FILL 3, NETWORK_ERROR 2, INTERNAL_ERROR 0, INVALID_REQUEST 1 |
| https://developers.google.com/admob/api/v1/report-metrics-dimensions | metric definitions: requests, matched requests, match rate, show rate, impressions |
| https://developers.google.com/admob/api/v1/report-overview | reporting API for network and mediation reports |
| https://support.google.com/admob/answer/13547458 | partner bidding changes match and show rate reporting |

## Callback name map

| Concept | iOS | Android | Flutter |
|---|---|---|---|
| ad dismissed | `adDidDismissFullScreenContent` | `onAdDismissedFullScreenContent` | `onAdDismissedFullScreenContent` |
| failed to show | `didFailToPresentFullScreenContentWithError` | `onAdFailedToShowFullScreenContent` | `onAdFailedToShowFullScreenContent` |
| impression | `adDidRecordImpression` | `onAdImpression` | `onAdImpression` |
| reward earned | `userDidEarnRewardHandler` | `onUserEarnedReward` | `onUserEarnedReward` |

The iOS dismiss, impression and reward names are on the iOS rewarded page; Android names are on the Android rewarded page; the Flutter dismiss and earned-reward names are on the Flutter rewarded page. The Flutter impression callback name and the iOS failed-to-present selector were not re-checked on a Flutter or iOS page in this pass: confirm in the SDK reference. React Native uses a third-party wrapper whose names this skill did not verify.

## Anthropic authoring guidance applied

Source: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices and https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview

- Name: lowercase letters, numbers and hyphens, 64 characters or fewer, gerund form (`serving-mobile-ads`), no reserved words.
- Description: third person, says what the skill does and when to use it, under 1024 characters, no XML tags.
- SKILL.md body under 500 lines; detail moved into reference files.
- References one level deep from SKILL.md; reference files over 100 lines open with a contents list.
- Workflows as copyable checklists, with an audit report format.
- No time-sensitive statements; platform facts are cited to pages to re-read instead of dated.
- One term per concept (vocabulary table in SKILL.md).
- Forward-slash paths, descriptive file names.
