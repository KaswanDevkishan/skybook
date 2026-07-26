## Why

SkyBook's current guest-booking form exposes seats across all flights and ends without
a price review or confirmation, so it does not provide a coherent reservation journey.
This change introduces the first major booking-flow redesign now that a later course
milestone explicitly permits the required schema and workflow expansion beyond the
Exercise 11 boundary.

## What Changes

- Add Economy and Business cabin classification, Window/Middle/Aisle seat types, and
  decimal JPY prices to seats through a data-safe Django migration.
- Store immutable base fare, taxes and fees, total price, a unique user-friendly
  booking reference, creation time, and any confirmation-supporting status on each
  booking.
- Extend idempotent demo seeding with varied classified and priced seats without
  rescheduling flights, changing bookings, or duplicating seats.
- Enrich complete-page and HTMX flight results with schedule details, duration,
  nonstop status, availability counts, cabin availability, lowest available price,
  and a flight-specific Book action only when seats remain.
- Refine flight search with a premium responsive hero, elevated search card,
  route-focused results, and a "View seats" action without changing search or booking
  behavior.
- Simplify shared navigation by keeping the SkyBook brand as the homepage link,
  removing the separate Home item, and retaining Flights as the only navigation item
  with its active-state, keyboard, and responsive behavior. Authentication navigation
  remains deferred to a separate future change.
- **BREAKING**: Remove the generic `/booking/new/` and `/booking/submit/` workflow from
  navigation and replace it with a flight-specific, server-validated path from flight
  selection through seat selection, passenger entry, price review, confirmation, and
  booking receipt.
- Restrict every seat choice and submitted seat identifier to the selected flight and
  current availability while retaining transactional and database-backed
  double-booking protection.
- Upgrade seat selection to a responsive aircraft-style map that groups database seats
  by cabin, row, and letter while retaining native radios, text states, keyboard
  operation, and a no-JavaScript submission path.
- Add accessible seat-detail tooltips and an optional vanilla-JavaScript selection
  summary with server-derived estimated JPY amounts; review and confirmation remain
  authoritative server steps.
- Calculate a documented JPY tax-and-fee rule authoritatively on the server and never
  accept browser-submitted prices as authoritative.
- Update tests and contributor documentation for the connected guest flow, pricing,
  migration, seed data, accessibility, SQLite development, and preserved Render
  production behavior.
- Keep accounts, real payments, copied airline branding, model-backed aircraft
  geometry, dashboards, cancellation, lookup, round trips, external APIs, and
  unrelated infrastructure or redesign work out of scope.

## Capabilities

### New Capabilities

- `connected-booking-workflow`: Flight-scoped seat selection, passenger entry,
  server-side price review, atomic confirmation, and the confirmation receipt.
- `booking-pricing`: JPY seat pricing, immutable booking-time amounts, the tax-and-fee
  rule, and unique booking references.

### Modified Capabilities

- `reservation-data-model`: Add classified and priced seats plus immutable booking
  price, reference, and timestamp data while preserving existing records.
- `reservation-forms`: Replace the generic all-flight seat form contract with
  flight-scoped validation and multi-step guest-booking inputs.
- `basic-reservation-views`: Replace generic booking routes with flight-specific
  booking and confirmation routes and simplify shared navigation.
- `server-driven-flight-search`: Enrich reusable flight results with availability,
  price, and conditional flight-specific booking actions.
- `accessible-responsive-interface`: Define accessible and responsive seat controls,
  review forms, errors, states, and focus behavior.
- `render-production-deployment`: Extend safe idempotent demo seeding while preserving
  SQLite/PostgreSQL selection and existing Render configuration.
- `django-project-foundation`: Update the course feature boundary to permit the
  connected booking workflow and its required schema changes.
- `repository-agent-guidance`: Record the new permitted booking-flow scope and keep
  future features and unrelated infrastructure deferred.

## Impact

The change affects reservation models and migrations, forms, pricing/domain services,
views and named URLs, database transactions, demo-data seeding, Django templates,
namespaced CSS and minimal vanilla JavaScript, existing HTMX result rendering, tests,
README documentation, and OpenSpec guidance. The aircraft map increment requires no
model or migration change: it is a progressive visual layer over flight-scoped native
form controls. The change adds no new web framework, payment provider, external API,
background service, or production infrastructure dependency; the resulting
migrations and behavior must work on both local SQLite and Render PostgreSQL.
