## 1. Confirm Schema and Authentication Foundation

- [x] 1.1 Inspect the built-in auth/session configuration and existing nullable
  `Booking.user` relationship on both Django model and migration state.
- [x] 1.2 Keep the built-in Django user model and create a reservation migration only if
  inspection and `makemigrations --check --dry-run` identify genuine schema drift.
- [x] 1.3 Define named registration, sign-in, POST sign-out, account, and guest My Bookings
  routes with fixed safe fallback destinations.

## 2. Build Registration and Session Flows

- [x] 2.1 Implement a `UserCreationForm`-based registration form for username, normalized
  unique email, first name, last name, password, and password confirmation using Django
  password validators and non-password field retention.
- [x] 2.2 Implement the CSRF-protected registration view to create the built-in user,
  establish a Django session after success, and redirect to the account page.
- [x] 2.3 Configure or carefully wrap Django sign-in behavior with generic invalid-login
  feedback and allow only same-host, scheme-safe `next` redirects.
- [x] 2.4 Implement a POST-only, CSRF-protected logout action that clears the session and
  redirects to a fixed public route without supporting state-changing GET.
- [x] 2.5 Create semantic registration and sign-in templates that never repopulate or
  expose submitted password values and render accessible field and summary errors.

## 3. Add Account History and Access Control

- [x] 3.1 Implement a login-required account view that renders the current user's name,
  email, username, and efficiently selected owned bookings only.
- [x] 3.2 Render account booking cards with reference, route, departure date, seat, whole-
  yen total, and booking status only when a status field is present, plus an empty state.
- [x] 3.3 Add the public guest My Bookings placeholder without querying booking data and
  route authenticated My Bookings requests to account history.
- [x] 3.4 Centralize confirmation visibility so member-owned receipts return 404 to
  anonymous and non-owner requesters while null-user guest receipts remain functional.

## 4. Associate Bookings and Preserve Passenger Edits

- [x] 4.1 Generalize the transactional booking creation service to accept an optional
  authenticated owner and assign it atomically while preserving seat locking,
  revalidation, unique references, authoritative JPY pricing, and database constraints.
- [x] 4.2 Pass `request.user` at final confirmation only when authenticated and retain
  `user=null` for anonymous guest checkout.
- [x] 4.3 Supply authenticated profile name and email as initial values only on an unbound
  passenger form, retaining empty initials for guests.
- [x] 4.4 Preserve edited passenger name and email across validation, review, final
  confirmation, and persistence so a signed-in user can book for another passenger.

## 5. Update Shared Navigation and Presentation

- [x] 5.1 Update the shared template so the brand links to the primary public entry and
  logged-out navigation contains Flights, My Bookings, Sign In, and Create Account.
- [x] 5.2 Render logged-in navigation with Flights, My Bookings, Account, and a semantic
  CSRF-protected POST Log Out form, with correct route-family active states.
- [x] 5.3 Extend the existing namespaced stylesheet with premium navy authentication
  cards, consistent controls and errors, readable account booking cards, nav-button
  parity, visible focus states, and responsive mobile behavior.
- [x] 5.4 Verify the new pages retain the shared skip link, semantic landmarks, visible
  labels, keyboard operation, accessible errors, and no site footer.

## 6. Test Authentication and Navigation

- [x] 6.1 Add tests for successful registration, password hashing and validation, password
  mismatch, duplicate username, case-insensitive duplicate email, malformed email, safe
  retained values, and absence of password values in rendered responses.
- [x] 6.2 Add tests for successful and failed sign in, Django session creation, allowed
  local `next`, rejected external or protocol-relative redirects, and generic failure
  feedback.
- [x] 6.3 Add CSRF-aware tests proving POST logout succeeds, GET is rejected without
  clearing the session, and a POST without CSRF returns 403.
- [x] 6.4 Add tests for anonymous account redirection, authenticated profile rendering,
  logged-out and logged-in navigation, active states, brand/home behavior, and both My
  Bookings destinations.
- [x] 6.5 Add template and static-asset tests for responsive auth/account structures,
  semantic landmarks, visible labels, accessible errors, keyboard focus rules, mobile
  navigation, and the absence of fake authentication links.

## 7. Test Ownership and Booking Regressions

- [x] 7.1 Add account-history tests proving a user sees only bookings whose `user` foreign
  key they own and cannot see another user's or email-matched guest booking.
- [x] 7.2 Add receipt tests proving owners can view member bookings, anonymous and other
  users receive 404, unknown references remain 404, and guest receipts still work.
- [x] 7.3 Add connected-flow tests proving authenticated confirmation stores
  `request.user`, anonymous confirmation remains a null-user guest booking, and submitted
  passenger values persist independently of the account profile.
- [x] 7.4 Add tests proving authenticated passenger details are initially prefilled,
  remain editable, survive invalid/review/confirmation submissions, and guest fields
  remain initially empty.
- [x] 7.5 Run and retain existing server-authoritative pricing, direct confirmation,
  database constraint, stale/concurrent double-booking, CSRF, HTMX/full-page search, seed
  idempotency, migration, SQLite, Render/PostgreSQL settings, WhiteNoise, health, static
  collection, and Gunicorn regressions.

## 8. Document Scope and Security

- [x] 8.1 Update README endpoint and behavior documentation for registration, sign in,
  POST sign out, authenticated navigation, account history, guest checkout, booking
  ownership, receipt authorization, and passenger prefill/editability.
- [x] 8.2 Document Django hashing, validators, sessions, CSRF, safe redirects, credential
  hygiene, and the absence of manual password storage.
- [x] 8.3 Document current limitations: no cancellation, guest booking lookup, payment
  redesign, flight tracking, external APIs, email verification, password reset, or
  historical guest-booking claiming.
- [x] 8.4 Update repository agent guidance to include the authentication and ownership
  milestone while retaining the established booking, deployment, demo-data, and
  out-of-scope invariants.

## 9. Verify the Completed Change

- [x] 9.1 Run `uv run ruff format .` and review the formatting diff.
- [x] 9.2 Run `uv run ruff check .`.
- [x] 9.3 Run `uv run python manage.py check`.
- [x] 9.4 Run `uv run python manage.py makemigrations --check --dry-run`.
- [x] 9.5 Run the complete `uv run pytest` suite and confirm coverage is not reduced.
- [x] 9.6 Run strict OpenSpec validation for
  `add-user-authentication-booking-ownership`.
- [x] 9.7 Run `git diff --check`, inspect the final diff for credentials or unrelated
  changes, and leave the change uncommitted, unpushed, and unarchived.

## 10. Add Status-Based Booking Cancellation

- [x] 10.1 Add Confirmed/Cancelled booking status with a safe historical Confirmed
  default and migrate the seat uniqueness constraint to apply only to Confirmed rows.
- [x] 10.2 Update every availability, seat-map, form, count, and booking-service query so
  only Confirmed bookings occupy inventory and cancelled seats can be rebooked.
- [x] 10.3 Add an owner-only future cancellation confirmation route and atomic,
  CSRF-protected, idempotent POST transition with non-leaking 404 authorization.
- [x] 10.4 Add the accessible cancellation page, account status badges and eligibility
  actions, clear rejection/success feedback, and simulated-payment/no-refund notice.
- [x] 10.5 Add migration, ownership, CSRF, GET/POST, history, inventory, rebooking, past,
  repeated-cancellation, guest-preservation, and snapshot-preservation tests.
- [x] 10.6 Update README and repository guidance for retained cancellation history,
  owner/future restrictions, released inventory, and absence of real refunds.
- [x] 10.7 Run formatting, lint, Django checks, migration drift, full tests, strict
  OpenSpec validation, and `git diff --check`; do not commit, push, or archive.

## 11. Gate Booking Completion on Authentication

- [x] 11.1 Add a minimal versioned pending-booking session contract containing only
  flight id, seat id, passenger name, and passenger email, with validation and cleanup
  for malformed or missing flight-scoped seat data.
- [x] 11.2 Update anonymous seat-selection POST handling to validate and preserve pending
  input, create no Booking, and redirect to Sign In or Create Account through a fixed
  safe local resume destination.
- [x] 11.3 Resume valid pending bookings after sign-in or registration, restore editable
  passenger details, recheck confirmed-seat availability, and recalculate authoritative
  JPY pricing from current database values before review.
- [x] 11.4 Require authentication at direct review and final confirmation boundaries,
  assign every newly completed public booking to `request.user`, and clear pending data
  after successful confirmation while preserving historical guest receipts.
- [x] 11.5 Update the seat-selection UI so anonymous users see the required notice,
  primary Sign in to continue button, and secondary Create account link while
  authenticated users see Review price.
- [x] 11.6 Remove any passenger-email User lookup or account-match validation and ensure
  passenger name and email remain editable and independent of the booking owner.
- [x] 11.7 Add tests for authentication-state UI, pending detail preservation, sign-in
  and registration resume, no pre-authentication Booking, direct request protection,
  unsafe next rejection, session cleanup, unavailable seats, database pricing,
  passenger-email privacy, unregistered passengers, and owned completion.
- [x] 11.8 Update README and repository guidance to document required authentication,
  passenger/account independence, non-disclosure, pending resume, historical guest
  compatibility, ownership, pricing, availability, and cancellation invariants.
- [x] 11.9 Run `uv run ruff format .`, `uv run ruff check .`,
  `uv run python manage.py check`, `uv run python manage.py makemigrations --check
  --dry-run`, the complete `uv run pytest` suite, strict OpenSpec validation, and
  `git diff --check`; do not commit, push, or archive.

## 12. Refresh Flight-Search Hero Copy

- [x] 12.1 Replace the flight-search eyebrow, heading, and description with the supplied
  journey copy while preserving the existing semantic structure, layout, typography,
  responsiveness, and accessibility.
- [x] 12.2 Update focused tests, README wording, and the active flight-search contract,
  including regression assertions that the replaced copy is absent.
- [x] 12.3 Run formatting, lint, Django checks, migration drift, the complete test suite,
  strict OpenSpec validation, and `git diff --check`; do not commit, push, or archive.

## 13. Show Active Bookings Only

- [x] 13.1 Filter the login-required account queryset by owner and Confirmed status so
  future and past Confirmed bookings remain visible while Cancelled bookings and their
  receipt links are absent from My Bookings.
- [x] 13.2 Update the account empty state to say “You have no active bookings.” while
  retaining the Find a flight action and cancellation success message.
- [x] 13.3 Add regression tests for confirmed/cancelled list visibility, retained
  cancelled data, cancellation redirect behavior, all-cancelled empty state,
  owner-only cancelled receipts, and released seat inventory.
- [x] 13.4 Update README documentation to distinguish active My Bookings display from
  internally retained Cancelled records.
- [x] 13.5 Run formatting, lint, Django checks, migration drift, the complete test suite,
  strict OpenSpec validation, and `git diff --check`; do not commit, push, or archive.

## 14. Improve Sign-In Error Presentation

- [x] 14.1 Replace duplicated failed-login output with the single friendly accessible
  alert while retaining field-specific validation directly beneath its associated input.
- [x] 14.2 Add responsive, overflow-safe alert styling within the sign-in card using the
  established SkyBook error palette and no positional or fixed-height workarounds.
- [x] 14.3 Add regression tests for single-message failure output, absence of raw
  duplicated Django text, alert semantics, field-error association, and unchanged
  successful login behavior.
- [x] 14.4 Run formatting, lint, Django checks, migration drift, the complete test suite,
  strict OpenSpec validation, and `git diff --check`; do not commit, push, or archive.

## 15. Flight-search entry point

- [x] 15.1 Replace the standalone homepage with a normal non-permanent Django redirect
  from `/` to `/flights/`, and make logout return to flight search.
- [x] 15.2 Link the shared SkyBook brand directly to `/flights/` while preserving the
  required logged-out and logged-in navigation entries.
- [x] 15.3 Remove the unused homepage view, template, and homepage-only styles without
  removing styles shared by flight search or authentication pages.
- [x] 15.4 Update route, navigation, landing-copy, logout, README, and OpenSpec tests and
  documentation for the flight-search entry point.
- [x] 15.5 Run formatting, lint, Django checks, migration drift, the complete test suite,
  strict OpenSpec validation, and `git diff --check`.

## 16. Reject Past Flight-Search Dates

- [x] 16.1 Set the departure-date input minimum from `timezone.localdate()` and add
  server-side field validation that rejects only dates before today with the required
  message.
- [x] 16.2 Preserve full-page and HTMX search behavior while returning no results for an
  invalid past date and associating the identical error with the date input.
- [x] 16.3 Add tests for the dynamic minimum, yesterday/today/future validation, no past
  results, both response modes, and a configured-timezone local-date boundary.
- [x] 16.4 Update README flight-search documentation to state that departure dates are
  limited to today and future dates.
- [x] 16.5 Run the complete test suite, Django checks, migration drift check, formatter,
  linter, strict OpenSpec validation, and `git diff --check`; do not commit, push, or
  archive.

## 17. Simplify Flight-Search Hero

- [x] 17.1 Remove the flight-search eyebrow and description while retaining only the
  supplied heading with the search form directly below it.
- [x] 17.2 Remove obsolete copy spacing and preserve the navy hero design, responsive
  layout, semantic heading association, and accessibility.
- [x] 17.3 Update focused tests, README wording, and the active flight-search contract
  so the removed copy is explicitly absent.
- [x] 17.4 Run formatting, lint, Django checks, migration drift, the complete test suite,
  strict OpenSpec validation, and `git diff --check`; do not commit, push, or archive.
