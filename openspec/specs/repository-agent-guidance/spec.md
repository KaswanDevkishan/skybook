# Repository Agent Guidance Specification

## Purpose

Define repository guidance that keeps SkyBook contributors and agents aligned with the
current Django architecture, course scope, tooling, domain constraints, review
expectations, and security requirements.
## Requirements
### Requirement: Consistent project identity
Repository guidance SHALL identify SkyBook as a Python 3.12, Django, SQLite airline
reservation course project and SHALL NOT direct contributors or agents to restore the
obsolete Flask scaffold or introduce another web framework.

#### Scenario: Agent selects a web framework
- **WHEN** an agent reads repository guidance before planning work
- **THEN** it finds Django identified as the required framework

### Requirement: Accurate repository and tooling guidance
Contributor documentation SHALL reflect the checked-in Django repository structure and
SHALL document the `uv` setup, migration, and server commands plus Ruff formatting,
Ruff linting, Pytest, coverage, Django system checks, and migration drift checks
configured by `pyproject.toml` and CI.

#### Scenario: Contributor verifies the project
- **WHEN** a contributor follows the documented quality commands
- **THEN** Django checks, migrations, formatting, linting, tests, and coverage run with
  the repository's configured tools

### Requirement: OpenSpec-first implementation workflow
Agent guidance and OpenSpec configuration SHALL require relevant OpenSpec documents to
be read before meaningful implementation and SHALL require focused implementation,
verification, and human review.

#### Scenario: Agent begins meaningful implementation
- **WHEN** an agent prepares to modify project behavior or structure
- **THEN** it first reviews the relevant OpenSpec artifacts and applies their
  constraints

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

### Requirement: Repository hygiene
Guidance and Git exclusions SHALL cover tokens, passwords, Render credentials,
`SECRET_KEY`, `DATABASE_URL`, `.env` files, virtual environments, caches, coverage
artifacts, collected static output, and local SQLite/database files, while making clear
that ignore patterns do not authorize storing secrets. Guidance SHALL also state that
Render's app-local filesystem is ephemeral and is not suitable for future persistent
uploaded media.

#### Scenario: Local development creates generated or sensitive files
- **WHEN** standard local environment, cache, coverage, secret, database, or collected
  static files appear
- **THEN** Git excludes them and contributor guidance says they must not be committed

#### Scenario: Contributor plans persistent media
- **WHEN** future application work requires user-uploaded files
- **THEN** repository guidance requires persistent object storage instead of relying on
  the web service filesystem
