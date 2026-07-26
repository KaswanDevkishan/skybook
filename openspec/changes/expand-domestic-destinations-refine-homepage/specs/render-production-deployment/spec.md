## MODIFIED Requirements

### Requirement: Safe course demonstration data initialization
SkyBook SHALL provide an idempotent `seed_demo_data` command that creates approximately
30–40 major Japanese airport or airport-served destinations, at least two airlines, a
curated set of connected domestic flights spanning every required Japanese region, and
seats for every seeded flight. Seeded seats SHALL include Economy and Business cabins,
Window/Middle/Aisle types, and varied positive whole-yen JPY prices. The command SHALL
use stable identities and non-destructive creation so repeated runs do not duplicate
records, delete or alter bookings, rename or replace cities, reschedule or reroute
existing flights, overwrite unrelated records, mutate existing seats, or create
duplicate seats.

#### Scenario: Empty production database is seeded
- **WHEN** the command runs after migrations on an empty database
- **THEN** representative nationwide search data and multiple classified, priced,
  bookable seats are available

#### Scenario: Seed command is repeated
- **WHEN** the command runs more than once with unrelated data and an existing booking
- **THEN** seeded records are not duplicated and existing bookings, city identifiers
  and values, unrelated records, flight endpoints and schedules, and seat identities
  and values remain intact

#### Scenario: Seeded price variation is inspected
- **WHEN** seats on newly seeded flights are listed
- **THEN** Economy and Business plus all three seat types are represented with enough
  positive whole-yen price variation to demonstrate lowest-price displays

#### Scenario: Deployment date advances
- **WHEN** the command runs during a later deployment
- **THEN** existing seeded flight endpoints and times remain unchanged while each
  missing flight is created with a future valid schedule relative to the later run

#### Scenario: Seed catalog is invalid
- **WHEN** configured seed data has duplicate identities, unknown endpoint codes,
  same-city routes, or non-positive durations
- **THEN** the command fails clearly before creating data

### Requirement: Deployment verification coverage
SkyBook SHALL retain automated coverage for production settings, static configuration,
migrations, search, and connected booking behavior and add destination, route,
preservation, seat, price, homepage, and footer coverage compatible with SQLite
development and PostgreSQL production. Release verification SHALL run the full test
suite, Ruff formatting and linting, Django checks, dry-run migration drift detection,
strict OpenSpec validation, and diff whitespace checks while retaining existing
production checks.

#### Scenario: Contributor verifies the expanded dataset and homepage
- **WHEN** the documented verification sequence is run
- **THEN** the new seed and interface regressions plus existing search, booking, and
  Render production settings tests pass without schema or deployment security changes
