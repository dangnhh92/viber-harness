# Testing, store assets, submission

## Testing

**Needed when:** before every TestFlight or Play upload.

**Not needed when:** a metadata-only version; it may go without a build test.

**Do it right:**
- "Tested" means every flow walked through the real UI on a simulator or device, with simulated data through real ingest. Every displayed number is checked against an independent oracle script, for both user and admin. Direct table writes are unit tests only, never integration tests.
- Derive every oracle figure from a written rule, never from the screen it checks.
- Reproduce review conditions: a fresh simulator (`xcrun simctl erase`), no sandbox account, slow or no network.
- Device first for anything involving consent, ATT, push, IAP or haptics. The simulator hides the UMP code 4 failure and has no push token.
- Look at every screenshot. Byte-identical "stills" and a test runner reporting COMPLETED on a blank screen are both common.
- Replay every external request live once. A request recorded with the wrong method fails silently.
- Never revert work because a device install half-failed; reinstall cleanly and re-check first.
- Never call work done with the core path stubbed.
- Flutter: `flutter install` alone ships a stale `Runner.app`; run `flutter build ios --release` first.
- Release-only Android crashes often come from R8 stripping JNI; add keep rules for any plugin with JNI.

**Check:** Is there an oracle script whose numbers match every number shown on screen in a walkthrough of each flow, on a fresh device, with screenshots inspected?

## Store screenshots and graphics

**Do it right:**
- Sizes: use the sizes the app's earlier accepted set used. If there is no earlier set and the user has not stated a size, ask; never guess. Sizes accepted before: iPhone 1284x2778 or 1242x2688 (landscape 2778x1284, 2688x1242), iPad 13" 2064x2752, Play phone 1080x1920. iPhone sets at 1320x2868 have been rejected; do not use it unless the user says so.
- At most 10 per size, no alpha channel [ASC-shots].
- Every screenshot is a marketing shot, never a raw capture:
  - A real in-app capture placed inside a phone frame. No fake UI.
  - A big headline in the store language stating one benefit.
  - Background and type in the brand palette colours.
  - The first slide is the hook, built on a real figure or the core value.
  - No prices, no "free", no "Premium" labels.
- The same rules apply to Play phone screenshots and the Play feature graphic (1024x500).
- App preview video: 886x1920, stereo AAC 48 kHz (mono is rejected).
- Grep store text, captions and UI for third-party trademarks (camera, film and brand names such as Polaroid, Kodak, Fuji) before any upload. Any hit blocks it.
- People in screenshots: free stock has no model release. Use AI-generated people or people who signed a release.
- Each IAP has its own promo image.
- Before submit, list every asset as current or stale against the build. Wait for anything still rendering; never submit stale previews.

## Android 12+ splash

**Needed when:** every Android app.

**Do it right:**
- Android 12+ draws the system splash from the launcher icon and masks it to a circle about two thirds of the icon box (icon without background: 288 dp box, 192 dp circle; with background: 240 dp box, 160 dp circle). Full-bleed art gets cropped.
- Ship an Android-specific splash image (`windowSplashScreenAnimatedIcon`) with the art padded inside the inner circle. Never reuse the iOS full-bleed splash.
- Keep the adaptive icon foreground inside the 66% safe zone (72 dp of the 108 dp layer).
- Check the cold-start first frame on an Android 12+ emulator: kill the app, launch, capture the first frame.

**Check:** Is the splash art whole inside the circle on that first frame, with no cropped edge?

## Store submission

**Needed when:** every submission. Never skipped.

**Do it right:**
- Description legal links:
  - The App Store description ends with `Privacy Policy: <the app's privacy policy URL>` and `Terms of Use: https://www.apple.com/legal/internet-services/itunes/dev/stdeula/` (Apple's standard EULA).
  - Play ends with the privacy line only.
  - Take the privacy URL from the app's repo, its store record or the user. If it is not known for certain, ask the user; never guess or build one from a domain pattern.
  - The privacy URL returns 200 (`curl -sI <url>`).
- Placeholder sweep: grep for `PLACEHOLDER|TODO|example.com|lorem|XXXX`, store links included (for example `idPLACEHOLDER`). Any hit blocks the build [ARG 2.1(a)].
- Deployment targets:
  - iOS: at least 15.0 (Firebase needs it), set in the Podfile and all three build configs. Check Apple's current upload SDK and minimum requirements before each submit.
  - Android `targetSdk`: the current Play target API floor. Read it from [Play-target] before each submit; never trust a remembered number.
  - `minSdk` from the real plugin floor, at least 24.
- Export compliance: `usesNonExemptEncryption=false` (`asc builds update --uses-non-exempt-encryption=false`).
- Version names: an approved version's name is closed; bump the name (a build-number-only re-upload fails with 90062/90186). Keep iOS and Android in lockstep.
- Play closed test: at least 12 testers opted in continuously for 14 days before production access [Play-test].
- Run `gplay validate` before `edits create`; validate deletes an open edit.
- 2.1 information requests: answer with a device recording from launch, permission prompts included, plus a numbered reply.
- Fix what the reviewer did, not just the text they cited.

**Check:** the pre-submit checklist in `SKILL.md`.
