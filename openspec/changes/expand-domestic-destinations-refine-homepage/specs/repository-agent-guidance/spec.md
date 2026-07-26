## MODIFIED Requirements

### Requirement: Current exercise scope boundary
Repository guidance SHALL identify the domestic-data and homepage milestone as
permitting approximately 30–40 stable major Japanese airport or airport-served
destinations, curated regional demonstration routes, non-destructive idempotent
flight/seat seeding, the supplied homepage hero copy, and complete footer removal. It
SHALL preserve the connected booking milestone, Django, full-page and HTMX search,
database duplicate-seat protection, immutable booking data, SQLite development, and
Render PostgreSQL behavior. It SHALL continue to prohibit accounts and authentication
navigation, real payments, exhaustive or live schedules, external airline APIs,
copied branding, model-backed aircraft geometry, unrelated redesign, Docker, Redis,
Celery, and workers.

#### Scenario: Agent implements the domestic data change
- **WHEN** an agent reads repository guidance before implementation
- **THEN** destination, route, seat, homepage, footer, preservation, and documentation
  work is permitted and the existing booking and deployment invariants are explicit

#### Scenario: Agent considers a later feature
- **WHEN** implementation would add authentication navigation, complete or live
  schedules, external APIs, payment, booking management, or unrelated infrastructure
- **THEN** guidance identifies that work as outside the current change

### Requirement: Domain constraints remain documented
Guidance SHALL identify `City`, `Airline`, `Flight`, classified and priced `Seat`,
Django's built-in authentication user, and immutable-price `Booking` as implemented
entities. It SHALL document stable unique destination codes, preservation of existing
destination rows and flight schedules, guest and registered-user data compatibility,
flight-scoped seat validation, authoritative JPY pricing, non-mutating repeated
seeding, and database-backed prevention of duplicate seat bookings.

#### Scenario: Agent reviews domestic booking requirements
- **WHEN** an agent reads project documentation
- **THEN** it can distinguish representative seeded destination and route data from a
  complete live schedule and can identify all preserved booking invariants
