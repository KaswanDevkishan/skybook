## Why

SkyBook's small demo dataset does not offer enough geographic variety to make domestic
flight search feel representative, and the homepage copy and footer no longer match the
focused connected booking experience. This later course change expands demonstration
coverage while preserving every existing destination, schedule, seat, and booking.

## What Changes

- Expand idempotent demo data to approximately 30–40 major Japanese domestic airports
  or airport-served destinations, using stable unique airport codes and clear English
  names while preserving all existing `City` rows and identifiers.
- Seed a curated, realistic set of demonstration routes spanning Hokkaido, Tohoku,
  Kanto, Chubu, Kansai, Chugoku, Shikoku, Kyushu, and Okinawa without attempting a
  complete route network or live schedule.
- Create future schedules only when each seeded flight is initially created; repeated
  seeding never reschedules an existing flight, duplicates a destination, flight, or
  seat, or modifies a booking.
- Give every newly seeded flight the existing Economy and Business seat structures and
  whole-yen JPY pricing through the existing idempotent seat creation behavior.
- Replace the homepage hero eyebrow, heading, and description with the supplied
  Japan-focused copy.
- **BREAKING**: Remove the complete site footer from shared page output and remove its
  now-unused styles and footer-specific tests.
- Keep the SkyBook brand as the homepage link and Flights as the current navigation
  item; continue to defer Sign In and Create Account navigation.
- Add preservation, idempotency, destination, route, seat, price, homepage, footer,
  search, and connected-booking regression coverage.
- Update README and active OpenSpec guidance to describe the major-airport demonstration
  dataset as neither complete nor a live aviation schedule.
- Keep authentication, external airline data, exhaustive route generation, live
  schedules, and unrelated interface changes out of scope.

## Capabilities

### New Capabilities

- `domestic-demo-data`: Major Japanese destination coverage, curated regional routes,
  and preservation-safe idempotent flight, schedule, seat, and price seeding.

### Modified Capabilities

- `reservation-data-model`: Require the seeded destination collection to use stable,
  unique airport codes while preserving existing destination records and relationships.
- `basic-reservation-views`: Update the homepage hero contract while preserving the
  connected flight-search and booking entry points and compact navigation.
- `accessible-responsive-interface`: Remove the footer landmark requirement and retain
  the remaining shared semantic, navigation, responsive, and accessibility guarantees.
- `server-driven-flight-search`: Ensure the expanded destination and route data remains
  usable by ordinary and HTMX search without changing their shared filtering contract.
- `render-production-deployment`: Extend the production-invoked demo seed contract with
  preservation-safe destinations, routes, seats, and prices.
- `repository-agent-guidance`: Record the authorized domestic dataset and focused
  homepage refinement while keeping authentication and external schedule features
  deferred.

## Impact

The change affects the `seed_demo_data` management command and its data definitions,
homepage and shared templates, namespaced CSS, seed/view/search/booking tests, README,
and OpenSpec guidance. It changes no model schema, migrations, public route, search
parameter, booking transaction, pricing rule, deployment service, database selection,
or dependency, and it must behave consistently with local SQLite and Render
PostgreSQL.

Related issues: `#<destination-issue>` and `#<homepage-issue>`.
