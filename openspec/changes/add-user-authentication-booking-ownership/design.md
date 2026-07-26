## Context

SkyBook already uses Django 5.2 sessions and the built-in user model indirectly through
the nullable `Booking.user` foreign key. Its connected booking flow currently validates
flight-scoped seats, reviews server-calculated JPY prices, and calls a transactional
guest-booking service that always leaves `user` null. Booking confirmations are retrieved
by a random reference without an ownership filter. The shared template has only a Flights
link, while the existing forms and navy visual system provide reusable accessibility and
responsive conventions.

This is a cross-cutting security change spanning forms, views, URLs, services, templates,
tests, documentation, and authorization. The older OpenSpec configuration still describes
Exercise 5's deferred screens, but the repository guidance and requested milestone now
explicitly permit Django-native authentication and account booking ownership. SQLite and
Render PostgreSQL must behave consistently, and the database-backed unique-seat constraint
must remain authoritative.

## Goals / Non-Goals

**Goals:**

- Provide registration, sign-in, CSRF-protected POST sign-out, and a login-required
  account page using Django's built-in authentication, hashing, validators, and sessions.
- Require authentication before price review and confirmation, and associate every newly
  completed public booking with the authenticated requester.
- Preserve safe pending passenger and seat input across sign-in or registration without
  treating passenger email as account identity.
- Restrict member My Bookings lists to the owner's active Confirmed bookings and member
  booking receipts to their owner.
- Let owners cancel their future confirmed bookings without deleting history, and return
  cancelled seats to inventory.
- Prefill passenger contact details for authenticated users without making them immutable
  or overwriting submitted edits.
- Render real account-aware navigation and accessible, responsive authentication and
  booking-history pages in the established visual language.
- Use flight search as the sole public entry page by redirecting `/` to `/flights/` and
  linking the SkyBook brand directly to `/flights/`.
- Preserve historical guest bookings and receipts plus the connected search, seat,
  pricing, confirmation, cancellation, HTMX, database, deployment, and duplicate-seat
  behavior.

**Non-Goals:**

- A custom user model, custom password hashing, social identity, email verification,
  password reset, or profile editing.
- Refunds, guest reference/email lookup, booking transfer, flight tracking, external
  APIs, or a booking/payment workflow redesign.
- Claiming historical guest bookings by matching their email to a new account.
- Passenger-email account discovery, an “Email not registered” error, or any other
  passenger-entry response that reveals whether an account exists.
- Changes to seeded flights, seats, prices, or production infrastructure.

## Decisions

### Use Django authentication primitives and a focused registration form

Registration will extend or compose `UserCreationForm` for the built-in user model,
adding required email, first name, and last name fields. It will call Django's normal
`save()` path so password hashing and configured validators remain authoritative. Email
will be normalized and checked case-insensitively for existing accounts; duplicate email
will be reported as ordinary registration validation without using email as a login
identifier. Successful registration will authenticate the newly created user with
`login()` and resume a valid pending booking when present, otherwise redirect to the
account page.

Using `UserCreationForm` is preferred over a hand-built password form because it preserves
Django's password validation and mismatch behavior. A custom user model or manual password
storage would add migration and security risk without serving this milestone.

### Use username-based Django login and an explicit POST logout view

The sign-in route will use Django's `LoginView` with a project template and a fixed safe
fallback destination. Django's authentication form and session framework will handle
credentials. The standard `next` mechanism will be honored only when
`url_has_allowed_host_and_scheme` accepts it for the current host and request scheme.
When a valid pending booking exists, successful sign-in will prefer the fixed local
booking-resume destination; an external or protocol-relative `next` value can never
override that destination.

Failed authentication will render one compact top-level alert with the fixed friendly
message “We couldn’t sign you in. Check your username and password and try again.” The
template will not also render Django's non-field error list or raw “Error:” labels.
Ordinary field validation remains attached beneath the relevant control. The alert will
stay within the authentication card and use the established error palette, consistent
spacing, readable line height, and overflow-safe responsive sizing without absolute
positioning, negative margins, or fixed heights.

Sign-out will be a POST-only, CSRF-protected view calling Django `logout()` and redirecting
to a fixed public route. Navigation will render it as a form/button, not a GET link.
This makes the state transition explicit and prevents cross-site logout links.

### Keep the built-in user schema and enforce registration email policy in the form

The built-in `User.email` column is not globally unique. This change will adopt a
case-insensitive "one newly registered account per email" policy in registration
validation while leaving existing users and the authentication schema intact. This avoids
introducing a custom user model after migrations already reference Django's user model.
The policy is an application-level registration guarantee rather than a new cross-table
database constraint; tests will cover ordinary duplicate submissions.

Changing `AUTH_USER_MODEL` now was rejected because it would create disproportionate
migration risk. Adding a database constraint directly to Django's managed auth table was
also rejected because it complicates portable migrations and could fail on pre-existing
duplicates.

### Generalize the transactional booking service with an optional owner

The authoritative creation service will accept an optional authenticated user and create
the booking with that owner inside the existing transaction. Passenger name and email will
continue to be stored in the existing guest contact fields even for an owned booking so
the immutable traveler/contact details can differ from the account holder. The service
will still lock/revalidate the seat, calculate the JPY amounts, generate the reference,
and rely on the unique-seat database constraint.

The booking view will pass `request.user` only when authenticated. This is preferred over
assigning ownership after creation because the booking must become owned atomically and
must never briefly exist as an unowned member booking.

### Apply passenger defaults only to an unbound initial form

On the initial GET, the view will build the passenger name from non-empty first and last
name values and use the account email as form initial data. A bound POST form will always
use submitted data. Review and confirmation will carry the validated passenger values
forward, and the server will never reapply profile defaults to a bound submission.

This permits booking for another passenger and avoids silently replacing an edit after a
validation error or between review and confirmation.

Passenger email is traveler/contact data, not an authentication identifier. Booking
forms and views will validate its syntax but MUST NOT query the user table with it,
compare it to `request.user.email`, display “Email not registered”, or otherwise reveal
whether it is assigned to an account.

### Store a minimal pending booking and resume through a fixed local route

When an anonymous visitor submits valid flight-scoped seat and passenger data, the
seat-selection view will store a versioned session payload containing only database
identifiers for the flight and seat plus passenger name and passenger email. It will not
store submitted price values, passwords, payment data, model objects, or an arbitrary
redirect. Separate “Sign in to continue” and “Create account” actions will save the same
validated payload and redirect to the selected authentication route with a fixed,
same-origin booking-resume `next` URL.

The resume route requires authentication. It will load the referenced flight and
flight-scoped seat from the database, clear malformed or missing-object session data,
recheck confirmed-booking occupancy, rebuild a bound booking form from the stored
passenger values, and recalculate the whole-yen price breakdown from current seat data.
Only then may it render price review. An unavailable seat returns the user to seat
selection with preserved safe passenger details and a visible availability error.

Pending data remains through review so final confirmation can revalidate it, and is
cleared after successful confirmation. This design avoids trusting client prices or
using passenger email to choose an authentication path.

### Require authentication at both review and confirmation boundaries

The public seat-selection GET remains available and editable for anonymous visitors, but
its anonymous primary action is “Sign in to continue”, accompanied by the notice “Sign
in or create an account to continue your booking.” and a secondary Create account link.
Authenticated users see “Review price”.

Review POST and final confirmation enforce authentication server-side. An anonymous
direct request is redirected to authentication after safe pending data is captured when
valid, and never calls booking creation. Final creation always receives
`request.user`; the optional-owner service signature may remain for historical/internal
compatibility, but no newly completed public booking can have a null owner.

### Centralize booking visibility rules

The account query will filter `Booking.objects` by both `user=request.user` and
`status=Booking.Status.CONFIRMED`, then select related flight data. Both future and past
Confirmed bookings remain visible. Cancelled bookings are excluded in the queryset rather
than hidden in the template, so they cannot render cards or receipt links. If no Confirmed
bookings remain, the dashboard displays “You have no active bookings.” and retains the
Find a flight action. The account route will use `login_required`. Confirmation lookup
will use a shared visibility rule:

- an owned booking is visible only when the requester is its authenticated owner;
- a guest booking remains accessible through its high-entropy booking reference so the
  existing guest receipt remains functional;
- anonymous or other authenticated requesters receive 404 for someone else's owned
  booking, avoiding both disclosure and an authorization oracle.

No account view will infer ownership by passenger email, and no predictable numeric
booking-detail URL will be added.

### Model cancellation as a status transition and active-only seat invariant

`Booking.status` will use Confirmed and Cancelled choices and default to Confirmed so the
migration safely classifies every historical row without altering its reference,
passenger, flight, seat, or price snapshots. Cancellation will lock and update the owned
booking atomically. Only an authenticated owner may reach the cancellation resource;
guest, unknown, and other-user references all receive the same non-leaking 404.

GET renders details and a warning but never changes state. POST is CSRF protected and
changes a future Confirmed booking to Cancelled. A past departure is rejected with a
clear message. Repeated POSTs are idempotent. The interface explicitly states payment is
simulated and no real refund occurs. Successful cancellation redirects to My Bookings,
where the confirmed-only account query immediately omits the cancelled record while the
success message remains visible. The cancelled receipt remains directly accessible to
its owner under the ordinary receipt authorization rule, but is not linked from the list.

The unconditional unique booking-per-seat constraint will become a conditional unique
constraint covering only Confirmed rows. Forms, seat maps, flight availability
annotations, and booking creation checks will likewise treat only Confirmed rows as
occupying seats. This keeps the database authoritative while retaining cancelled rows.

### Render navigation from authentication state with route-family active states

The shared Django template will branch on `request.user.is_authenticated`. Logged-out
users receive Flights, My Bookings, Sign In, and Create Account. Logged-in users receive
Flights, My Bookings, Account, and a POST Log Out form. My Bookings routes to account
history for members and to a public placeholder explaining that guest lookup is not yet
available. Route names or an explicit page context value will drive `aria-current`.

The existing CSS will be extended with namespaced auth, account, nav-form, and booking-card
styles plus narrow-screen behavior and visible focus rules. No unrelated flight-page
redesign or client framework is needed.

### Make flight search the canonical entry page

The root URL will use a non-permanent Django redirect to the named flight-search route.
The shared SkyBook brand will link directly to that route on every complete page. The
standalone homepage view, template, homepage-only styles, and landing-copy tests will be
removed because they duplicate the flight-search entry experience. The root route name
may remain as a compatibility handle for reversing `/`, but it will render no template.
Logout will redirect to the same public flight-search destination.

### Keep the canonical flight-search hero concise

The flight-search hero will retain its navy visual treatment and responsive, accessible
heading association while presenting only “Take off toward your next adventure” above the
search form. The former eyebrow and descriptive paragraph will be removed, along with
their reserved spacing, so the form follows the heading directly without changing the
search interaction or result-update behavior.

### Validate departure dates against Django's current local date

The flight-search form will derive the date input's `min` attribute each time it is
constructed from `timezone.localdate()`, so browser calendars follow `USE_TZ` and the
configured project timezone without a hardcoded date. A field cleaner will independently
reject any submitted date before the same local-date boundary with “Departure date cannot
be in the past.” Today and future dates remain valid.

Invalid searches will use an empty flight queryset and will not evaluate the normal
flight-results query. The complete page will render the error beneath the date field.
Because HTMX replaces only the results region, the partial will render the identical
message with a stable error ID referenced by the date input's `aria-describedby`
attribute. This preserves the existing HTMX target, progressive enhancement, form
styling, and focus treatment without alerts or client-side-only enforcement.

### Test security boundaries and preserve deployment regressions

Tests will cover password validation without asserting unstable validator prose, CSRF,
allowed and rejected `next` targets, method restrictions, navigation states, account
query isolation, receipt isolation, pending-session safety, sign-in and registration
resume, direct anonymous review protection, owned creation, editable passenger data
without user-email lookup, pricing, seat conflicts, and current Render settings.
Credentials in tests will be synthetic constants and will never be rendered back or
logged.

## Risks / Trade-offs

- [Case-insensitive email uniqueness has no new database constraint] → Normalize and
  validate in one registration form, document the policy, and avoid unsafe auth-table
  migrations; reassess with a custom user model only in a separate future change.
- [Ownership filtering could break guest confirmations] → Branch on persisted
  `Booking.user_id`, retain reference-based access for null-user bookings, and add both
  guest and member receipt tests.
- [Profile defaults could overwrite a traveler entered by the account holder] → Supply
  defaults only to unbound forms and regression-test invalid, review, and confirmation
  submissions with edited values.
- [Adding an owner could weaken guest-data constraints or duplicate-seat safety] → Store
  passenger contact independently, assign the owner inside the existing atomic service,
  and retain database constraints and concurrent-conflict handling.
- [POST logout in navigation can be styled inconsistently or become inaccessible] → Use a
  semantic form and button with the same focus, responsive, and visual treatment as nav
  links.
- [Authentication responses can reveal account data] → Keep sign-in errors generic,
  return 404 for unauthorized receipts, and expose duplicate emails only as normal
  create-account validation.
- [Passenger email could become an account oracle] → Treat it only as validated contact
  data, never query User from booking input, and test registered and unregistered
  passenger emails through identical booking behavior.
- [A pending seat can become unavailable during authentication] → Store identifiers only,
  requery the database and recheck confirmed occupancy before review and confirmation.
- [Session state can become stale or attacker-controlled] → Use a small versioned schema,
  reject malformed values, clear missing flight/seat data, and never store prices,
  credentials, payment data, or arbitrary redirect targets.
- [Cancellation could race with rebooking] → Lock the booking/seat transactionally and
  retain a database conditional uniqueness constraint for Confirmed bookings.
- [Client date constraints can be bypassed or use the wrong calendar day] → Derive both
  the HTML minimum and server validation boundary from Django's timezone-aware local date
  and cover a timezone-boundary case in tests.

## Migration Plan

1. Add booking status with a Confirmed default, preserving all historical booking data,
   and replace unconditional seat uniqueness with confirmed-only uniqueness.
2. Add forms, URLs, views, pending-session/resume behavior, ownership-aware service and
   cancellation behavior, templates, and CSS.
3. Add tests and documentation, then run the full quality and strict OpenSpec checks.
4. Deploy through the existing Render build/migration/start process; Django's existing auth
   tables and sessions require no new service.

Rollback removes the new routes/templates and pending-session behavior. Existing owned
and historical null-user bookings remain valid because the nullable relationship
predates this change; historical guest receipts remain readable.

## Open Questions

None. Password reset, email verification, stronger database-level normalized email
uniqueness, guest lookup, and refunds are deliberately reserved for later changes.
