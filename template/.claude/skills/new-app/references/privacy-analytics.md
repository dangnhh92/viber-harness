# Privacy, analytics, startup, localization

## Privacy manifest and Data safety

**Needed when:**
- Every iOS app that uses a required-reason API (UserDefaults, file timestamps, and others) or ships an SDK that collects data needs `PrivacyInfo.xcprivacy`. App Store Connect rejects uploads missing the reasons [ReqReason; PrivManifest].
- Every Play app on closed, open or production tracks needs Data safety [Play-DS].

**Not needed when:** Play apps only on the internal testing track [Play-DS].

**Do it right:**
- Add the manifest in Xcode via File > New File > App Privacy, on the app target, so it lands in bundle resources. Do not add it by script (the xcodeproj gem produced a wrong path and a failed archive).
- AdMob apps: leave `NSPrivacyTracking` false or absent in the app's own manifest; the App Privacy label carries the tracking declaration. `true` with no tracking domains gets ITMS-91064.
- The App Privacy label declares at least what bundled SDKs collect: Device ID, coarse location, advertising data, product interaction, crash data. A manifest saying "no tracking, no data" while ATT or analytics run is wrong.
- Data safety includes SDK collection, crash logs and pseudonymous diagnostics. "Encrypted in transit" only if all traffic is [Play-DS].
- The privacy policy page matches the build and Data safety: consent line, crash/diagnostics line, encryption-in-transit line, date. Its URL returns 200 on a live domain.
- Answer the age rating from the code (accounts, chat, UGC), not from memory.
- Data safety has an API (`gplay data-safety`). IARC rating, target audience, ads and AI-content declarations are console-only: give the owner a fill-in sheet.
- After a Play edit, confirm Data safety is actually set and the app is not left Unpublished (there is no API to republish).

**Check:**
- Does `PrivacyInfo.xcprivacy` exist in the archived app?
- Do the App Privacy label, Play Data safety and the privacy page list the same data types?
- Does the privacy URL return 200?

## Analytics, crash reporting and startup

**Needed when:** every shipped app needs crash reporting. Analytics only for decisions someone will make from it [invented].

**Not needed when:** analytics events nobody reads. Every event is also a Data safety line [Play-DS].

**Do it right:**
- Never await analytics or Crashlytics before first paint. Use `unawaited()`; report only in release.
- Boot steps sit in try/catch and always reach `runApp` (or the root render).
- Never await a network call (Remote Config, consent, settings) before the splash leaves. Add a hard fallback timer of 8 s.
- Declare Crash Data on the label when Crashlytics ships; verify dSYM upload on the first archive.
- Compute metrics from data that account deletion does not erase.
- Await server-side alert calls on serverless; an unawaited call is dropped when the function exits.
- Enable App Store analytics reports (ONGOING) for every iOS app.

**Check:** With the network off, does a cold launch reach the home screen within 8 s, and does a forced test crash appear in the console with symbols?

## Localization

**Needed when:** the owner names a market.

**Not needed when:**
- Store copy defaults to en-US only. Add en-GB or vi only when the owner asks.
- ASO-only locales (keywords with no in-app translation) need explicit owner approval.

**Do it right:**
- The app's default language matches its store default. Every permission string is in that language, with `InfoPlist.strings` per extra locale.
- Native-speaker copy needs a voice sample or a reference app; without one it reads as translationese.
- Release-build guard: fail on any string in the wrong language.
- Slogans never name a platform. Platform names appear only in functional instructions.
- Check text by Unicode code point (hexdump), not by how the terminal renders it; look-alike characters fool the eye.
- Vietnamese keywords: words longer than 2 characters; the field is 100 bytes, not 100 characters.
- `asc metadata push` deletes every locale missing from the folder. Pull first and dry-run; the dry run must show zero deletes.

**Check:** Is every store locale one the owner approved, and did the metadata dry run show zero deletes?
