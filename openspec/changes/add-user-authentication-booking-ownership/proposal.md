## Why

SkyBook supports passenger entry before authentication but must not use passenger email
as an account-discovery mechanism or allow anonymous booking completion. This change adds
Django-native authentication and safely connects every newly completed public booking to
its authenticated owner while preserving historical guest bookings and the existing
search-to-seat-selection workflow.

## What Changes

- Add Create Account, Sign In, CSRF-protected POST Log Out, and login-required Account
  flows using Django's built-in user model, password hashing, validators, sessions, and
  safe redirect handling.
- Collect username, email, first name, last name, password, and password confirmation at
  registration; require a unique email address for new accounts without changing the
  built-in user model or creating custom password storage.
- Add an account dashboard that displays only the signed-in user's profile and active
  Confirmed owned bookings, including future and past departures, reference, route,
  departure, seat, and total. Cancelled records remain stored internally but do not
  render in My Bookings.
- Add owner-only cancellation for future confirmed bookings through a confirmation page
  and CSRF-protected POST. Cancellation changes persisted status to Cancelled rather than
  deleting history, releases the seat to inventory, redirects to My Bookings where the
  record immediately disappears, and performs no refund because payment remains simulated.
- Require authentication before price review and final confirmation, and associate every
  newly completed public booking with `request.user`.
- Let logged-out visitors select a seat and enter passenger details, then safely preserve
  only flight, seat, passenger name, and passenger email in the session while they sign
  in or create an account; do not create a Booking before authentication.
- Resume the pending booking after sign-in or registration, revalidate the flight and
  seat, recheck availability, and recalculate pricing from database values.
- Prefill authenticated passenger name and email only when initially presenting passenger
  details, leave both editable, and preserve submitted edits through review and
  confirmation so an account holder may book for someone else. Never query accounts from
  passenger email or disclose whether that email belongs to an account.
- Make booking-receipt access ownership-aware: authenticated bookings are available only
  to their owner, and predictable references cannot reveal another user's booking.
- Replace placeholder authentication navigation with responsive, accessible logged-out
  and logged-in variants; route My Bookings to account history for members and to a clear
  future-lookup message for guests.
- Remove the standalone homepage, redirect `/` to `/flights/`, and make the shared
  SkyBook brand link directly to flight search.
- Add focused templates and premium navy styling for authentication and account pages
  without redesigning unrelated flight-search or booking pages.
- Add comprehensive authentication, navigation, ownership, prefill, security, regression,
  documentation, and deployment-configuration tests.
- Limit flight searches to today and future departure dates using Django's current local
  date for both the native date-input minimum and server-side validation, with matching
  accessible errors in complete-page and HTMX responses.
- Preserve historical null-user guest bookings and their high-entropy receipts while
  keeping HTMX search, seat selection, authoritative JPY pricing, simulated
  payment/review, atomic duplicate-seat protection, cancellation, SQLite development,
  and Render PostgreSQL behavior intact.
- Keep dummy-payment redesign, booking-flow redesign, refunds, guest booking lookup,
  flight tracking, external APIs, custom authentication models, and custom password
  storage out of scope.

## Capabilities

### New Capabilities

- `user-authentication`: Registration, sign-in, POST sign-out, session security, safe
  redirects, and authentication-aware shared navigation.
- `account-booking-ownership`: Account profile and owned-booking history, required
  authenticated booking association, pending-booking resume and cleanup, access control,
  historical guest receipt compatibility, and editable passenger details independent of
  account identity.

### Modified Capabilities

- `reservation-forms`: Add account registration and sign-in validation contracts,
  initial-only authenticated passenger defaults, editable passenger fields, and a strict
  prohibition on passenger-email account lookup or disclosure.
- `basic-reservation-views`: Add authentication/account routes and account-aware shared
  navigation, plus authentication-gated review and pending-booking resume.
- `accessible-responsive-interface`: Define accessible, responsive authentication cards,
  account booking cards, errors, navigation actions, keyboard behavior, and focus states.
- `django-project-foundation`: Update the course feature boundary to permit built-in
  authentication screens, account views, and booking ownership behavior.
- `repository-agent-guidance`: Record authentication and booking ownership as current
  scope while retaining cancellation, guest lookup, and unrelated future features as
  explicit non-goals.

## Impact

The change affects Django forms, authentication-backed views and named URLs, session
state, booking review and confirmation access checks, shared context/template navigation,
authentication and account templates, homepage cleanup, namespaced CSS, tests, README
documentation, and OpenSpec guidance.
The existing nullable `Booking.user` relationship supports ownership. A safe migration
adds Confirmed/Cancelled booking status, defaults historical rows to Confirmed, and
replaces the unconditional seat uniqueness rule with a confirmed-booking-only constraint.
No new web framework, identity provider, password implementation, payment integration,
client-side framework, background service, or production infrastructure dependency is
introduced; behavior must remain portable across SQLite and Render PostgreSQL.
