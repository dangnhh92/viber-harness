# Measuring ad loading

## Contents
- Metric definitions
- Two failure directions
- Client events
- Client ratios
- AdMob-side pull
- Reading the pair
- Starting targets
- Audit hits

## Metric definitions

From the AdMob API metrics list (https://developers.google.com/admob/api/v1/report-metrics-dimensions):
- `AD_REQUESTS`: the number of ad requests.
- `MATCHED_REQUESTS`: "The number of times ads are returned in response to a request."
- `MATCH_RATE`: "The ratio of matched ad requests over the total ad requests."
- `SHOW_RATE`: "The ratio of ads that are displayed over ads that are returned, defined as impressions / matched requests."
- `IMPRESSIONS`: "The total number of ads shown to users."

Match rate answers "did AdMob have an ad". Show rate answers "did the app use what it got".
- Low match rate: no-fill, or requests made at bad times (offline, before consent, regions or states without demand).
- Low show rate: loads the app never used.

Caveat from AdMob help: for partner bidding ad units matched requests are calculated differently, so match rate can drop and show rate rise without any change in revenue. Read the report for the setup in use. Source: https://support.google.com/admob/answer/13547458 (AdMob help, partner bidding glossary).

Google's checklist of common causes of low match rate (blocking controls, high eCPM floors, policy enforcement, child-directed apps, crashes, traffic changes) is at https://support.google.com/admob/answer/9655701. Rule those out before blaming loading code.

Per-key aggregation (per app, platform, format): requests = sum of requests, matched = sum of matched, match rate = matched / requests, show rate = impressions / matched, eCPM = earnings / impressions * 1000. Re-run before quoting any figure: all of these are dated observations.

## Two failure directions

- **Waste** = loads never shown. Measured by show rate.
- **Starvation** = moments where an ad could have been shown and none was ready.

A change that improves one must be checked against the other. Cutting loads raises show rate and can raise starvation. Loading earlier lowers starvation and can wreck show rate.

## Client events

Wire these before shipping. Names are suggestions; keep one naming scheme.

| Event | Fields | Purpose |
|---|---|---|
| `ad_load_requested` | format, trigger | request volume per trigger |
| `ad_load_filled` | format, ms | fill latency |
| `ad_load_failed` | format, domain, code, nofill | split no-fill from errors |
| `ad_load_skipped` | format, reason (offline, consent, session_cap, held, in_flight) | prove the guard works |
| `ad_shown` | format, placement | from the SDK impression callback only |
| `ad_show_failed` | format, code | present failures |
| `ad_expired` | format | held ads lost to lifetime |
| `app_open_opportunity` | trigger, ready | logged when the show checks pass, before show or skip |
| `app_open_skipped` | reason | why not |
| `rewarded_offer_shown` | reason, ready | starvation numerator and denominator |
| `rewarded_ready_late` | ms | fill landed while the offer was open |
| `rewarded_accepted` | placement | offer conversion |
| `rewarded_earned` | placement | reward grants |

## Client ratios

- Show rate (waste) = `ad_shown / ad_load_filled` per format.
- Starvation, rewarded = `rewarded_offer_shown{ready:false}` that never got a `rewarded_ready_late`, divided by all `rewarded_offer_shown`.
- Starvation, App Open = `app_open_opportunity{ready:false} / app_open_opportunity`.
- Offer conversion = `rewarded_accepted / rewarded_offer_shown{ready:true}`.
- Load latency = median of `ad_load_filled.ms`.

## AdMob-side pull

Use the AdMob reporting API (https://developers.google.com/admob/api/v1/report-overview) or the console report. Filter by app, platform and format, compute per format as above. Judge a change after two to four weeks, never on day one: a correct change shows requests falling sharply while earnings do not. Roll-outs are gradual because users update at their own pace, so the cleanest month is the first full month after most users updated.

## Reading the pair

- Low show rate and low starvation together: the load condition is too early.
- High starvation with a healthy match rate: the load condition is too late, or fill is slow.
- High starvation with a low match rate: no-fill. No client change fixes it; check `nofill: true` versus `false` in `ad_load_failed`. Dominant `nofill: true` is demand; dominant `nofill: false` is requests fired offline or before consent.
- Request count falling while impressions hold or rise: the intended outcome of moving loads to intent.

## Starting targets

These are starting hypotheses taken from the best rows of one practitioner portfolio, not Google benchmarks. Set targets from your own baseline and have someone other than the implementer ratify them.

| Metric | Starting target | Too low means | Too high means |
|---|---|---|---|
| Rewarded show rate | 50% or more | loading too early, or a load path fires with no condition | fine |
| Rewarded starvation | 15% or less | fine | loading too late, or slow fill: check match rate and latency first |
| App Open show rate | 40% or more | few qualifying returns inside the lifetime (normal for once-a-day users); do not add load moments | fine |
| App Open starvation | 40% or less | fine | loads not surviving to the return: check `ad_expired` count |
| Match rate | 70% or more where demand exists | with `nofill: true` dominant: demand, not code | fine |
| Rewarded median load latency | 3 s or less | fine | threshold must move earlier, not the offer wait longer |

Illustration: in one portfolio the best rewarded rows reached roughly 50 to 70% show rate; the worst were near 1 to 3%. The starvation numbers above were never measured by that portfolio; they are guesses to be replaced.

## Audit hits

- Impression logged before the show call.
- No `ad_load_failed` event with a no-fill flag.
- Only request counts tracked, no show rate.
- Targets set by the party that implemented the change.
