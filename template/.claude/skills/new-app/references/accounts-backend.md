# Support, accounts, push, security, backend

## Contents
- In-app feedback and support
- Sign-in, account deletion, Apple revoke
- Push notifications
- Security (secrets, backend, OWASP MASVS)
- Backend data, performance and operations

## In-app feedback and support

**Needed when:** every app needs a contact path [ARG 1.5]. Apps with accounts or money need an in-app channel.

**Not needed when:** a small offline game; a Support URL plus an email on the privacy page can be enough [invented].

**Do it right:**
- Tickets go to the admin console. The admin replies in-app to signed-in users and by email to signed-out users. mailto is not a replacement for in-app support.
- The signed-out support form never fails closed; it is the only route to a human. Rate-limit it per sender, with a global ceiling.
- Read store reviews per country (iTunes lookup/RSS; `google-play-scraper`); drop reviews older than the current build.

**Check:** Does the Support URL return 200 and show a contact method, and (account apps) does a signed-out ticket reach the console?

## Sign-in, account deletion, Apple revoke

**Needed when:** only when the app has significant account-based features [ARG 5.1.1(v)].

**Not needed when:** offline games and tools with no backend. Anonymous auth (for a leaderboard) still creates an account record: decide deletion for it too, and declare it truthfully in Data safety.

**Do it right:**
- Offering Google or any third-party login means also offering Sign in with Apple, or another login that collects only name and email and lets the user hide their email [ARG 4.8].
- The Sign in with Apple button is no smaller than the others and needs no scrolling [HIG-siwa].
- Let people explore before sign-in [HIG-onboarding].
- Account deletion [ARG-del]:
  - In-app, easy to find, usually in account settings.
  - Deletes the whole account and its data; deactivation alone fails review.
  - No phone, email or chat step.
  - Applies to guest accounts too.
  - Styled as destructive, with a cancel. Test it end to end on a release build; it is a common crash point.
- Subscribers are told billing continues through Apple; offer `showManageSubscriptions` [ARG-del].
- Apple revoke: use the Sign in with Apple REST API at deletion time with a fresh authorization code; store no Apple token. If the revoke fails, offer to delete anyway and record it.
- Play requires an in-app deletion path and a web deletion link, entered in the Data safety form. All data declared there is in scope [Play-del].
- Google sign-in on iOS with Supabase: `useIdTokenAuthRequest` returns no id_token on native. Use the code flow: send `sha256(nonce)`, call `exchangeCodeAsync`, pass the raw nonce.
- Supabase links identities by verified email. Give any admin account an unverifiable address (for example `.internal`) so it never absorbs a real user's sign-in.
- Google OAuth clients and the consent screen have no API. Send the owner one prefilled sheet: package, SHA-1 of the upload key and of the Play signing key, redirect URIs.
- Google sign-in on Android with `expo-auth-session`: pass `androidClientId`. Without it the request falls back to the Web client and Google blocks it ("Custom scheme URIs are not allowed for 'WEB' client type", 400). Create one Android client per signing key (Play signing and upload), each with "Enable custom URI scheme" on under Advanced settings, and add every Android client id to the Supabase Google provider's client id list, since the id token's audience is the Android client.
- Never delete `Podfile.lock`; it floats GoogleSignIn and AppAuth to new versions and can block a release.
- A migration and the function that uses it deploy together.
- Never report deletion as done while any step is stubbed.

**Check:**
- Can a fresh account sign in with Apple, delete itself in-app, and show the Apple revoke in the audit row?
- Does the Play web deletion link return 200?

## Push notifications

**Needed when:** a time-relevant event the user asked to hear about.

**Not needed when:**
- Marketing without explicit in-app opt-in [ARG 4.5.4; HIG-notif].
- The app has no server-side events [invented].

**Do it right:**
- Permission timing per the permissions section. Push is never required to use the app [ARG 4.5.4].
- Promotional push needs separate explicit consent and an in-app opt-out. Never the Time Sensitive level for marketing [HIG-notif].
- One provider for both platforms (for example Expo push).
- The APNs key must be created with the APNs service enabled; a key's services are fixed at creation. A Sign in with Apple `.p8` returns 403 InvalidProviderToken.
- Put tap-routing data where the client reads it (Expo: under `body`). A rendered banner is never evidence that the payload is right.
- Deploy the token-register migration before the client that calls it.
- A push that depends on a state change fires at the event that causes it (for example the import), not on app open. A push feature needs its scheduler or trigger built before the task closes.
- Simulator builds have no `aps-environment` and never get a token; use `xcrun simctl push` for banner shots only.
- Android "FCM accepted" but nothing arrived: force-stop kills delivery, tokens rotate, a foreground banner is suppressed by design, `pm clear` revokes `POST_NOTIFICATIONS`.

**Check:** On a real iPhone with a TestFlight build, does a server-sent push arrive and does tapping it open the intended screen?

## Security (secrets, backend, OWASP MASVS)

**Needed when:** always. Backend items apply only when there is a backend.

**Not needed when:** certificate pinning (MASVS-NETWORK-2) and anti-tamper (MASVS-RESILIENCE) for apps with no money, accounts or sensitive data [invented]. The MAS L1 profile mapping is unverified; the baseline uses the MASVS v2 control list.

**Do it right** [MASVS]:
- STORAGE-1/2: store sensitive data securely; never leak it to logs or backups. Tokens in Keychain/Keystore (SecureStore), never AsyncStorage or SharedPreferences [invented detail].
- CRYPTO-1/2: platform crypto only.
- AUTH-1: a server-side check on every privileged action.
- NETWORK-1: TLS for all traffic.
- PLATFORM-2: lock down WebViews.
- CODE-1/3: current platform and dependencies without known CVEs.
- CODE-4: validate every untrusted input server side.
- PRIVACY-1..4: minimize data, be transparent, give control.
- Secrets never ship in the app. No server keys in the bundle; the Supabase service key is server-only [Supa-RLS].
- Briefs pass credentials by file path, never by contents. Agents never read `.env*`, `*.p8` or service-account JSON.
- RLS on every table in an exposed schema; default-deny until policies exist. Write `(select auth.uid())` in policies [Supa-RLS].
- `SECURITY DEFINER` functions get `search_path = ''` and stay out of exposed schemas [Supa-RLS].
- Revoke `EXECUTE` from `public`, `anon` and `authenticated` on every new function; assert it with `has_function_privilege`.
- RLS gates access, never amounts. A money figure never depends on the caller's cached plan.
- Rate limits live in Postgres or Upstash with a row lock (atomic check-and-write), never an in-memory Map on serverless and never read-then-write.
- Admin login is rate-limited too.
- Rewards and purchases are granted only from verified server callbacks (SSV, receipt validation).
- Firebase rules validate value ranges and reject extra fields.
- Deploy the migration before the code that needs it, enforced by a pre-push hook.

**Check:**
- Does `grep -rE "service_role|sk_live|BEGIN PRIVATE KEY"` over the app source return nothing?
- Does `get_advisors` (security) report no RLS-disabled table?
- Does an anon `has_function_privilege` check return false for every privileged function?

## Backend data, performance and operations

**Needed when:** the app has a database, imports external data, or moves money.

**Not needed when:** fully offline apps.

**Do it right:**
- Run the Supabase advisors (security and performance) before every release; ship with zero WARN. Typical findings: policies calling `auth.uid()` per row instead of `(select auth.uid())`; two permissive SELECT policies (admin plus own) where one merged policy would do; foreign keys without an index; link tables without a primary key; Auth DB connections fixed at 10 instead of a percentage.
- Scale test before launch: seed realistic volume, `EXPLAIN (ANALYZE, BUFFERS)` every app, console, function and cron query, and compare totals as well as times. Targets: a member read at most 100 ms, a console aggregate at most 1 s.
- Sum in the database; never fetch rows and add them in code.
- Every paged read orders by a unique key; unordered pages double-count at scale.
- Supabase (PostgREST) cuts every list read at `max_rows`, 1000 by default, with no error; the cap also cuts embedded child lists and set-returning RPCs. A history, log, order or transaction table passes 1000 rows early. Every read of a growing table either pages with `.range()` or aggregates in SQL (an RPC, or `count: 'exact', head: true`). Audit every read: app, console, server routes, edge functions, cron jobs, exports. Prove each one with a seed of more than 1000 rows against an independent SQL count.
- A total shown beside a paged list comes from its own aggregate over the whole filtered set, never from the rows on the current page.
- Filters and sorts run in SQL, never on fetched rows; a filter applied after the fetch only sees the first 1000 rows. Admin lists have an explicit default sort (newest first) and keep filters in the URL.
- Filter by the member explicitly even under RLS. RLS stays the authority; the filter lets Postgres use the index.
- Keep derived values derived (compute on read) until a measurement shows a read over its target. A stored summary is a second truth that can drift. Check equality in tests, never by recomputing in production.
- Estimate cost, not only speed: CPU per query x users x opens per day, peak per second, then the compute size and price that carries it.
- Importing external data: before mapping a status, pair a real export with the API for the same window and take the field whose values match what the partner's UI shows.
- An unknown or malformed row is refused alone; every other row imports; the refusal is a warning on the admin log screen. One surprise never stops the pipeline.
- Write the full state table for every external status with the money effect of each (pending, completed, cancelled, changes after maturity up and down).
- Stuck-state alarms on the admin home: no successful import for N hours, items past their wait still not matured, a scheduled job not run, notifications unsent. Prove each fires on seeded broken data.
- Answer data questions by reading the stored data, not by reasoning about it.

**Check:**
- Do both Supabase advisors report zero WARN?
- Does the scale seed meet every read target, with totals matching the oracle?
- Does every read of a growing table return the same count as SQL on a seed of more than 1000 rows?
- Does a plan guard test fail on a deliberately dropped index?
