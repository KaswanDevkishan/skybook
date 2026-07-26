## 1. Domain Model and Pricing

- [x] 1.1 Add `Seat` cabin-class and seat-type `TextChoices` plus validated whole-yen
  Decimal pricing, and add immutable Decimal amounts, unique reference, and creation
  timestamp to `Booking` without adding an unnecessary status state.
- [x] 1.2 Implement and unit-test the shared 10% `ROUND_HALF_UP` JPY pricing function,
  including rounding boundaries and rejection of browser-supplied price authority.
- [x] 1.3 Implement and test readable `SKY-` booking-reference generation, database
  uniqueness, bounded collision retry, and useful model representations.

## 2. Data-Safe Migration

- [x] 2.1 Generate a staged schema/data migration that classifies and prices every
  existing seat, snapshots every existing booking at the documented fallback fare,
  assigns unique references and timestamps, and then enforces final constraints.
- [x] 2.2 Add migration-executor tests proving existing seats, relationships, guest and
  registered bookings, one-booking-per-seat protection, and final values survive the
  forward migration.
- [x] 2.3 Verify the migration uses backend-portable Django operations for SQLite and
  PostgreSQL and that migration reversal/rollback limitations are documented.

## 3. Demonstration Data

- [x] 3.1 Update `seed_demo_data` with stable Economy and Business seats covering
  Window, Middle, and Aisle types and varied realistic JPY prices.
- [x] 3.2 Test empty-database seeding and repeated seeding for no duplicate seats,
  unchanged flight schedules, unchanged existing bookings, preserved unrelated data,
  and adequate price/class/type variation.

## 4. Flight Search Results

- [x] 4.1 Build a reusable ORM/query helper that supplies available-seat counts, lowest
  available prices, available cabins, duration, and nonstop presentation without
  per-flight query growth.
- [x] 4.2 Update the reusable results partial so both full-page and strict
  `HX-Request: true` responses show airline, flight number, route, times, duration,
  nonstop state, lowest price, seats remaining, and cabin availability.
- [x] 4.3 Add a clear flight-specific Book link only when a seat remains and test
  lowest-price/count accuracy, selected-flight URL identity, sold-out omission,
  empty states, filtering, and progressive full-page/HTMX parity.

## 5. Flight-Scoped Booking Domain

- [x] 5.1 Replace the generic booking form with a flight-scoped Django form that
  validates passenger name/email and limits selectable seats to the URL flight's
  current unbooked seats.
- [x] 5.2 Implement a focused atomic booking service that revalidates flight ownership
  and availability, recalculates prices, generates a reference, persists guest
  snapshots, and maps stale/concurrent uniqueness failures to a seat conflict.
- [x] 5.3 Test valid guest creation, registered-user model compatibility, invalid
  flight identifiers, unknown seats, cross-flight injection, already-booked seats,
  direct final submissions, server-side price authority, reference collisions, and
  transaction/database double-booking prevention.

## 6. Connected Views and Routes

- [x] 6.1 Add named flight-specific booking and reference-specific confirmation URLs,
  remove the generic booking URLs, and enforce supported methods and 404 behavior.
- [x] 6.2 Implement GET seat selection, POST passenger/seat review, atomic final POST,
  and Post/Redirect/Get confirmation while retaining safe values and accessible
  errors on invalid or raced submissions.
- [x] 6.3 Build the review with complete itinerary, seat classification, base fare,
  taxes and fees, and total JPY details, all sourced authoritatively from the server.
- [x] 6.4 Build the confirmation receipt with reference, guest, itinerary, seat,
  immutable prices, and return-to-search link.
- [x] 6.5 Add view tests for each workflow state, CSRF protection, no persistence at
  review, exactly one booking at confirmation, confirmation details, unknown
  references, unsupported methods, and guest booking compatibility.

## 7. Accessible Responsive Interface

- [x] 7.1 Build semantic seat groups ordered by Business/Economy and row, using native
  radio controls for available seats and explicit disabled/unavailable presentation
  with number, type, price, and non-color state text.
- [x] 7.2 Add namespaced responsive CSS for seat cards, passenger/review/receipt
  layouts, error states, and visible `:focus-visible` behavior at mobile widths.
- [x] 7.3 Keep the flow fully operable without JavaScript; add only optional vanilla
  JavaScript enhancement and preserve ordinary GET search plus existing HTMX fallback.
- [x] 7.4 Test semantic groups, labels and error associations, alert/live semantics,
  keyboard-native controls, focus styling/static assets, explicit state text, and
  responsive class structure.

## 8. Navigation, Documentation, and Scope

- [x] 8.1 Remove every standalone Booking Form navigation item and generic booking
  action, retaining the linked SkyBook brand and Flights without adding placeholder
  navigation.
- [x] 8.2 Update README public-route and setup documentation for the connected flow,
  whole-yen Decimal pricing, Economy/Business behavior, 10% half-up fee rule,
  reference generation, guest booking, migrations, idempotent seeding, and simulated
  payment limitations.
- [x] 8.3 Update repository guidance to authorize this milestone while keeping
  aircraft SVG, accounts, dashboards, lookup, cancellation, round trips, real
  payments, external APIs, and unrelated infrastructure or redesign out of scope.
- [x] 8.4 Test removed generic navigation/routes and retain the existing SQLite
  defaults, Render PostgreSQL/settings, WhiteNoise, proxy security, health check,
  Blueprint, static collection, and Gunicorn WSGI coverage.

## 9. Verification

- [x] 9.1 Run `uv run ruff format .` and review that formatting touched only intended
  implementation and test files.
- [x] 9.2 Run `uv run ruff check .`.
- [x] 9.3 Run `uv run pytest` with no coverage regression.
- [x] 9.4 Run `uv run python manage.py check`.
- [x] 9.5 Run `uv run python manage.py makemigrations --check --dry-run`.
- [x] 9.6 Run strict OpenSpec validation for `redesign-connected-booking-flow`.
- [x] 9.7 Run `git diff --check`, review the complete diff for scope and secret
  hygiene, and leave the change uncommitted, unpushed, and unarchived pending live
  verification and human review.

## 10. Flight Search Presentation Refinement

- [x] 10.1 Build the complete-page travel hero and elevated three-field search card,
  retaining labels, validation, HTMX attributes, live feedback, and ordinary GET
  progressive enhancement.
- [x] 10.2 Redesign the reusable flight results as responsive route cards with
  hours/minutes duration, prominent minimum fare, availability and cabin summaries,
  conditional flight-scoped "View seats" actions, and sold-out behavior.
- [x] 10.3 Polish shared SkyBook/Flights navigation without adding deferred
  features.
- [x] 10.4 Add focused tests for the hero/search structure, duration formatting,
  CTA wording and sold-out omission, responsive classes, HTMX partial parity, shared
  navigation, readable content width, and connected booking workflow preservation.
- [x] 10.5 Run formatting, lint, Pytest, Django checks, migration drift detection,
  strict OpenSpec validation, and `git diff --check`; keep the change unarchived and
  uncommitted.

## 11. Visual Test Follow-up

- [x] 11.1 Remove the complete How it works section, its Search/Choose/Reserve cards,
  related styling, and obsolete test expectations without leaving trailing spacing.
- [x] 11.2 Restore a readable 72rem desktop content width with consistent hero gutters
  while preserving responsive three-, two-, and one-column flight results and no
  horizontal overflow.
- [x] 11.3 Remove the duplicate S brand mark so shared navigation displays only
  SkyBook, and add focused layout, branding, and absence tests.
- [x] 11.4 Run formatting, lint, Pytest, Django checks, migration drift detection,
  strict OpenSpec validation, and `git diff --check`; keep the change unarchived,
  uncommitted, and unpushed.

## 12. Aircraft Seat Map Upgrade

- [x] 12.1 Update proposal, design, capability specifications, and repository scope
  for a data-driven aircraft map that progressively enhances native form controls.
- [x] 12.2 Derive safe cabin, row, letter, availability, and server-calculated estimate
  view data from the selected flight without changing models or booking authority.
- [x] 12.3 Build the semantic aircraft-map template with fuselage cues, cabin sections,
  dynamic headings and rows, native labelled radios, disabled booked seats, detail
  tooltips, legend, selection summary, and passenger sidebar.
- [x] 12.4 Add namespaced responsive styling and optional vanilla JavaScript for
  desktop sticky-sidebar, tablet stacking, mobile map scrolling, sticky mobile action,
  visible focus, touch targets, and non-color state communication.
- [x] 12.5 Add focused tests for map structure, data grouping, seat headings and rows,
  available/selected/unavailable semantics, disabled labels, summary and JPY content,
  flight scoping and injection rejection, workflow preservation, static assets, and
  responsive classes.
- [x] 12.6 Run the full requested formatting, lint, test, Django, migration-drift,
  strict OpenSpec, and diff-whitespace verification; leave the change uncommitted,
  unpushed, and unarchived.

## 13. Navigation Simplification

- [x] 13.1 Update proposal, design, and relevant capability specifications so the
  linked SkyBook brand is the sole homepage navigation affordance, Flights is the only
  primary navigation item, and authentication navigation remains deferred.
- [x] 13.2 Remove the separate Home navigation item while preserving the SkyBook
  homepage link, Flights active-state semantics, keyboard focus, touch targets, and
  responsive behavior.
- [x] 13.3 Update focused navigation tests to cover the linked brand, Flights-only
  primary navigation, absence of Home and Sign in items, current-page semantics,
  keyboard-accessible links, and responsive styling.
- [x] 13.4 Run the full formatting, lint, Pytest, Django, migration-drift, static
  collection, deployment-check, strict OpenSpec, and diff-whitespace verification;
  leave the change uncommitted, unpushed, and unarchived.
