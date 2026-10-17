---
name: iap-entitlement
description: Rules and a required test matrix for in-app purchase and subscription entitlement on any stack (StoreKit 2, Google Play Billing, Flutter in_app_purchase, react-native-iap or expo-iap, cordova-plugin-purchase, RevenueCat, a custom server). Use when building, changing, reviewing or auditing any code that sells, grants, caches, restores or revokes a purchase, subscription, Remove Ads, Pro tier or consumable currency, and when writing the brief for such work. Load it in addition to new-app, never instead of it.
---

# IAP entitlement

Goal: the app grants exactly what the store says the user owns right now. Two failure directions, both real:

- **Fail open**: a user who does not own it (expired, refunded, never paid) gets it. Lost revenue, refund abuse.
- **Fail closed**: a user who paid loses it (grace, offline, store hiccup, unacknowledged and auto-refunded). Angry reviews, refunds.

A rule below names which direction it prevents. Unclear direction means unknown data: see rule 6.

## Vocabulary

| Term | Meaning |
|---|---|
| entitlement | the boolean or tier the app acts on (`isPro`, `noAds`, coin balance) |
| source of truth | the one record entitlement is derived from: store transactions on device, or the server row |
| cached flag | a stored copy of entitlement (prefs, localStorage, DB column) used before the source answers |
| re-derive | compute entitlement from the source of truth, overwriting the cached flag |
| grant event | a purchase stream or listener callback carrying a transaction |

## Rules

Each rule is checkable by reading code. In an audit, cite `file:line` for every rule, pass or fail.

### Source of truth

1. **One source, one derivation function.** Every path that sets entitlement (launch, resume, grant event, restore, server request) calls the same `deriveEntitlement(transactions, now)`. Prevents: one path checking expiry while another does not.
2. **Entitlement is a function of `now`, evaluated at every read that matters**, not a flag set once. A subscription has an end time; the app (or the server, per request) compares it with the current time. Prevents: Pro that never expires because nothing ever turned it off.
3. **Server apps enforce on the server, per request.** If a backend gates the feature, it checks `now <= period_end (+ grace)` on every request, not only at verify time. The client flag is display only. Prevents: Pro granted at purchase and never expired server-side.
4. **Cached flag is a hint, never authority.** It may show the UI instantly at cold start; it is overwritten by the first successful re-derive. It is never used to unlock something the source of truth was asked about and denied. Prevents: a stale `true` living forever.

### Expiry and dates

5. **Read dates as numbers, not formatted strings.** Use epoch milliseconds or seconds from the signed payload (`expiresDate`, `revocationDate` in the StoreKit 2 JSON, `expiryTimeMillis` / `lineItems[].expiryTime` from Play). Never `DateTime.parse` / `new Date()` a locale-formatted string. Prevents: Buddhist or Japanese calendar years, 12-hour overrides, and plugin format changes turning expiry into garbage.
6. **Unreadable means not entitled for that transaction.** A missing, null or unparseable expiry on a subscription transaction grants nothing from that transaction; log it. Prevents: fail open on every format change.
7. **Pin the IAP plugin version exactly** (no caret) and re-run the date tests on every bump. Prevents: a dependency upgrade silently changing a field format.
8. **Compare in UTC**, both sides epoch. Prevents: off-by-timezone expiry.

### Refund and revoke

9. **A transaction with a revocation date or a refund grants nothing**, on every path: launch scan, grant event, restore. On iOS check `revocationDate`; on Play treat a purchase missing from `queryPurchasesAsync` or present in the Voided Purchases API as gone. Prevents: refund keeps Pro.
10. **Grant events are not proof of a new purchase.** A listener can deliver refunds, revocations, old renewals and family-sharing changes with a "purchased" status. Run every event through rule 1 before granting or toasting "Pro is now active". Prevents: a refund that turns Pro on.
11. **Non-consumables can be revoked too** (refund, family sharing removed). Re-derive them like subscriptions; a one-way `= true` is a defect unless the owner decided otherwise in writing. Prevents: refund abuse of Remove Ads.
12. **Decide refunded-content policy explicitly** (for example "a picture started under Pro stays unlocked") and record it. Prevents: the builder guessing.

### Re-check timing

13. **Re-derive at launch, on every return to foreground, and when a grant event arrives.** Throttle foreground checks (at most once per 15 minutes is enough) but never skip them. Background audio, navigation or downloads keep a process alive for days. Prevents: a lapse while the app stays alive keeps Pro until the process dies.
14. **Re-derive on a timer only while the gated feature is in use** if sessions can outlast a period (a player app running for hours). Prevents: the same lapse inside one long foreground session.
15. **No race guard may block a later correction.** A "just purchased, ignore the next stale read" guard expires after one derive or a short window, and never applies to an event that is itself expired or revoked. Prevents: a stale event arming the guard and the correction being dropped.

### Grace and offline

16. **Billing grace counts as entitled** when the product has Billing Grace Period on (iOS: renewal state `inGracePeriod`, which `currentEntitlements` includes; Play: grace state is returned by `queryPurchasesAsync`). Account hold, paused and expired do not. Prevents: fail closed on a card retry.
17. **A store or network error keeps the last derived value**, it does not set `false` and does not set `true`. Only a successful answer changes entitlement. Prevents: fail closed offline, and fail open from a cached `true` being re-asserted.
18. **Cache a successful availability check, never a failed one.** Re-check `isAvailable` / billing connection on each buy, restore and resume. Prevents: one cold-start failure disabling purchases for the whole session.

### Android acknowledge

19. **Acknowledge or consume every purchased item wherever it is found**: purchase callback, launch query, resume query, restore. Play auto-refunds anything unacknowledged after 3 days. Pending purchases (`PENDING`) are neither granted nor acknowledged until they become `PURCHASED`. Prevents: paid purchases silently refunded when the app was killed mid-purchase.
20. **Query purchases on launch and on resume** (`queryPurchasesAsync`); the purchase listener does not redeliver purchases made while the app was not listening. Prevents: purchases made from a Play promo or while killed never granting.

### Grants, consumables, restore

21. **Consumables are granted once per transaction id.** Store the id with the grant in one atomic write, then finish/consume. On redelivery, finish without granting again. Prevents: double coins after a crash or failed consume.
22. **Grant first, then finish.** Never finish or consume before the grant is persisted. Prevents: paid and lost.
23. **Paid balances live in durable storage** (native preferences, a file, or the server), not a WebView `localStorage` the OS may clear. Prevents: paid coins vanishing with no store record to restore from.
24. **Grant only from the store result or the server, never from the `buy()` return value.** `buy()` returning means the sheet opened, not that money moved. Prevents: grant on cancel or pending.
25. **Restore re-derives; it never only adds.** iOS: Restore only from a Restore row (it can prompt for an Apple Account). Android: re-derive silently at launch. Prevents: restore that grants an expired sub.
26. **Unverified transactions grant nothing** (StoreKit 2 `.unverified`, bad signature, wrong bundle id, wrong package). A receipt status 0 proves it is genuine, not that it is for this app, this user, or still active. Prevents: forged or cross-app receipts.
27. **One original transaction id belongs to one account** on server apps. Prevents: one receipt unlocking Pro on many accounts.

### Server notifications

28. **Server apps subscribe to App Store Server Notifications v2 and Play RTDN** and apply `EXPIRED`, `REFUND`, `REVOKE`, `DID_FAIL_TO_RENEW`, `GRACE_PERIOD_EXPIRED`, `DID_RENEW`, `DID_CHANGE_RENEWAL_PREF`, `RENEWAL_EXTENDED` (Play: `SUBSCRIPTION_EXPIRED`, `SUBSCRIPTION_REVOKED`, `SUBSCRIPTION_ON_HOLD`, `SUBSCRIPTION_RECOVERED`, `SUBSCRIPTION_RENEWED`, voided purchases). Prevents: server state that only moves at verify time.
29. **Notifications are applied by event time, not arrival order.** Ignore a notification whose `signedDate` / event time is older than the one that produced the stored state; a refund is never overwritten by an older renewal. Prevents: out-of-order notifications resurrecting a refunded period.
30. **Notifications are not the only path.** Per-request expiry (rule 3) still holds when a notification is lost. Prevents: a missed webhook meaning Pro forever.

## Required tests for every IAP change

Every case runs through the real derivation function with injected transactions and an injected clock. Feed the payload exactly as the pinned plugin or API produces it, plus the malformed variants. "Green suite" counts only if every row below exists.

| # | Case | Expected |
|---|---|---|
| T1 | Expired subscription (expiry 1 minute ago) | not entitled |
| T2 | Live subscription (expiry in 1 day) | entitled |
| T3 | Refunded or revoked subscription, expiry still ahead | not entitled, no "active" toast |
| T4 | Refunded non-consumable | not entitled (or the recorded policy) |
| T5 | Renewed: old transaction expired plus a newer live one | entitled |
| T6 | Upgraded or crossgraded within the group: old product revoked by upgrade, new product live | entitled to the new tier only |
| T7 | Billing grace: expiry passed, renewal state in grace | entitled |
| T8 | Account hold or grace ended | not entitled |
| T9 | Unreadable date: null, empty, Buddhist year, AM/PM suffix, epoch string, wrong unit | not entitled from that transaction |
| T10 | Offline or store error with cached `true` | keeps last derived value, no grant, no revoke |
| T11 | Offline or store error with cached `false` | stays `false` |
| T12 | Resume after the expiry passed while backgrounded | not entitled after resume |
| T13 | Restore: one live sub, one expired, one refunded | only the live one |
| T14 | Android unacknowledged purchase found at launch or resume | acknowledged once, granted |
| T15 | Android pending purchase | not granted, not acknowledged |
| T16 | Consumable redelivered with the same transaction id | granted once, finished |
| T17 | Grant event delivering an expired or revoked transaction | no grant, race guard not armed |
| T18 | Server: request after `period_end + grace` | rejected as free tier |
| T19 | Server: refund notification, then an older renewal notification | stays refunded |

Device or sandbox checks (StoreKit configuration file or sandbox account) confirm the wiring, not the logic: purchase, restore, refund from the StoreKit transaction manager, accelerated renewal to expiry.

A StoreKit configuration file is a simulation. IAP passes only after real purchases with a sandbox tester account against the products in App Store Connect, on a device or a signed-in simulator. A tester that already owns a non-consumable (Lifetime) never sees the paywall again, and clearing its purchase history did not remove the Lifetime even 3 hours later. Use a fresh tester per paywall run; the App Store Connect API cannot create one, so the owner creates it on the web. When Restore shows "Apple Account Verification" and fails, sign the tester out and back in under Settings, Developer, then retry; it is account state, not an app bug. When Apple's sign-in needs a code sent to the owner's phone, ask for it once; never call IAP passed without the real run.

## Stack notes (known traps only)

**StoreKit 2 (Swift)**
- `Transaction.currentEntitlements` already excludes refunded, revoked and expired, and includes `inGracePeriod`. Prefer it for re-derive.
- `Transaction.all` includes every renewal and refunded or revoked transactions. Filtering it by hand requires checking `revocationDate` and `expirationDate` yourself.
- `Transaction.updates` delivers revocations and renewals. Check `revocationDate` before granting.
- Finish every verified transaction, or `Transaction.unfinished` redelivers it at each launch.

**Flutter `in_app_purchase` (`in_app_purchase_storekit`, `in_app_purchase_android`)**
- `SK2Transaction.expirationDate` is a String whose format depends on the plugin version: 0.4.8 and 0.4.10 format it with `DateFormatter` and no fixed locale (device calendar, device hour cycle); 0.4.13 sends milliseconds since epoch as a string. Read `expiresDate` and `revocationDate` (epoch ms) from `jsonRepresentation` instead.
- The StoreKit 2 bridge sends every `Transaction.updates` item to `purchaseStream` as `PurchaseStatus.purchased`, refunds included.
- `SK2Transaction.transactions()` wraps `Transaction.all` (refunded and expired included). On SK2, `restorePurchases()` emits `currentEntitlements` as `restored`.
- Android: `purchaseStream` does not redeliver purchases at launch. Call `queryPastPurchases()` and `completePurchase()` on each result where `pendingCompletePurchase` is true.
- A caret constraint (`^0.4.0`) lets `flutter pub upgrade` change the date format. Pin exactly.

**Google Play Billing (native, Billing 7 and 8)**
- Acknowledge within 3 days or Play refunds. `queryPurchasesAsync` returns active and grace subscriptions only; on hold and paused are absent.
- `queryPurchaseHistoryAsync` is removed in Billing 8. Do not build restore on it.
- Pending purchases need `enablePendingPurchases`; never grant `PENDING`.

**react-native-iap / expo-iap**
- `finishTransaction` must be called for every purchase, with `isConsumable: true` for consumables, or Android auto-refunds and iOS redelivers.
- The purchase listener fires only while mounted. Call `getAvailablePurchases` at launch and on foreground to catch purchases made while it was not.
- Server verification of the iOS JWS or Play token is the source of truth on server apps; the client purchase object is not.

**cordova-plugin-purchase v13 (Capacitor)**
- `approved` fires again at each launch for owned non-consumables and for any transaction not yet finished. Grants keyed by product id only double-grant consumables when `finish()` fails or the app dies before it.
- Without a validator there is no revoke event. Re-derive non-consumables from `store.owned()` after the receipts load successfully.
- WebView `localStorage` can be cleared by the OS. Keep paid balances in `@capacitor/preferences` or a file.

**Server (App Store Server API, Play Developer API)**
- Verify the JWS chain to Apple Root CA G3 and check bundle id, environment and `signedDate`. Production must accept sandbox for App Review.
- Play: `purchases.subscriptionsv2.get` gives `subscriptionState` and `lineItems[].expiryTime`; use it, not the client claim.
- Store `original_transaction_id` unique per account. Store event time per row for rule 29.

## Audit output

For each app: inventory line (stores, products, stack, server or client-only), then one row per rule 1 to 30 with `file:line` and pass, fail or n/a, then per defect: severity, platform, concrete failure scenario (who, what, how long), fix, and which test row (T1 to T19) proves it.
