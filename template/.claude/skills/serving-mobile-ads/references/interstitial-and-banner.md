# Interstitial and banner: generalizable lessons

Scope: only lessons that held across several apps. The core rules in SKILL.md apply unchanged (guard, expiry, ladder, consent, test ads).

## Interstitial

Google facts (https://developers.google.com/admob/ios/interstitial):
- "Because ads expire after an hour, you should clear this cache and reload with new ads every hour."
- "Interstitials should be displayed during natural pauses in the flow of an app" (the end of a task, between levels).
- "Make sure that users aren't so frequently interrupted that they're no longer able to enjoy the use of your app."
- "Load interstitial ads in advance to ensure they are ready to be shown without delay." Each interstitial is single use; "a best practice is to load another interstitial ad" after dismiss.

Lessons from practice:
- **Preload suits a frequent trigger.** An interstitial shown every few minutes by several triggers behind one cooldown reached the best show rate in one portfolio (about 70%). The same preload with a rare trigger wasted most loads (about 10 to 40% show rate), for example an ad loaded at splash for a game over reachable only after several levels. Match the load moment to how often the trigger fires. Rare trigger: load on intent, as for rewarded.
- **One cooldown across triggers.** Several triggers share one minimum gap so users are never double-interrupted.
- **No flat retry.** An interstitial retried on a fixed 60 second timer with no cap and no error branch behaved like the rewarded loop: low match rate in zero-fill states and wasted requests. Use the ladder and the no-fill stop from [loading-and-expiry.md](loading-and-expiry.md).
- **Load after consent and SDK start.** One app fired its first interstitial load before the SDK start and before consent.

## Banner

- **Cap the retry, expect no-fill on a new app.** A new, unapproved app or unit returns mostly no-fill (one brand-new app saw about 3% match over hundreds of requests). A banner retried every 60 seconds forever only inflates request count. See [consent-and-testing.md](consent-and-testing.md) for new app and unit timing.
- **Request only while the banner is on screen.** A hidden or backgrounded banner has no intent.
- **No test switch in the shipped bundle.** Same rule as every format.

## Not generalizable (left out on purpose)

- Placement count versus revenue: a single anecdote from a casual-game report that this skill could not verify.
- Region-specific demand figures: demand varies by region and time; measure your own with `nofill` split in events.
