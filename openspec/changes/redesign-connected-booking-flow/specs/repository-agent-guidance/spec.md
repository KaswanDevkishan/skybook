## MODIFIED Requirements

### Requirement: Current exercise scope boundary
Repository guidance SHALL identify the new booking-flow milestone as permitting seat
cabin, type, and JPY price schema; immutable booking-time amounts and references;
idempotent classified seed seats; enriched flight results; flight-specific accessible
seat selection; passenger entry; server-authoritative review; atomic guest
confirmation; and receipt display. It SHALL preserve Django, existing search and HTMX
fallback, database duplicate-seat protection, SQLite development, and Render
production behavior. It SHALL permit a CSS aircraft-style map that progressively
enhances native controls and SHALL continue to prohibit accounts, real payments,
copied airline branding, model-backed aircraft geometry, dashboards, cancellation,
guest lookup, round trips, tracking, external APIs, unrelated redesign, Docker,
Redis, Celery, and workers.

#### Scenario: Agent implements the booking redesign
- **WHEN** an agent reads repository guidance before implementation
- **THEN** the connected workflow and required schema are permitted and its preserved
  invariants and exclusions are explicit

#### Scenario: Agent considers a later feature
- **WHEN** implementation would add payment, accounts, aircraft data models, booking
  management, external APIs, copied branding, or unrelated infrastructure
- **THEN** guidance identifies that work as outside the current change

### Requirement: Domain constraints remain documented
Guidance SHALL identify `City`, `Airline`, `Flight`, classified and priced `Seat`,
Django's built-in authentication user, and immutable-price `Booking` as implemented
entities. It SHALL document guest and registered-user data compatibility,
flight-scoped seat validation, authoritative JPY pricing, and database-backed
prevention of duplicate seat bookings.

#### Scenario: Agent reviews booking requirements
- **WHEN** an agent reads project documentation
- **THEN** it can distinguish implemented booking guarantees from deferred account,
  payment, and booking-management behavior
