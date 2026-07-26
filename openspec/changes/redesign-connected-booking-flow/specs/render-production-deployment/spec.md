## MODIFIED Requirements

### Requirement: Safe course demonstration data initialization
SkyBook SHALL provide an idempotent `seed_demo_data` command that creates at least four
cities, at least two airlines, multiple connected future flights, and seats for every
seeded flight. Seeded seats SHALL include Economy and Business cabins,
Window/Middle/Aisle types, and varied realistic whole-yen JPY prices. The command SHALL
use stable identities and non-destructive operations so repeated runs do not duplicate
records, delete or alter bookings, reschedule existing flights, overwrite unrelated
records, or create duplicate seats.

#### Scenario: Empty production database is seeded
- **WHEN** the command runs after migrations on an empty database
- **THEN** search data and multiple classified, priced, bookable seats are available

#### Scenario: Seed command is repeated
- **WHEN** the command runs more than once with unrelated data and an existing booking
- **THEN** seeded records are not duplicated and existing bookings, unrelated records,
  flight schedules, and seat identities remain intact

#### Scenario: Seeded price variation is inspected
- **WHEN** seeded seats are listed
- **THEN** Economy and Business plus all three seat types are represented with enough
  price variation to demonstrate lowest-price displays

#### Scenario: Deployment date advances
- **WHEN** the command runs during a later deployment
- **THEN** existing seeded flight times remain unchanged while missing flights are
  created relative to the current date

#### Scenario: Seeded route is invalid
- **WHEN** configured seed data uses the same origin and destination
- **THEN** the command fails clearly before creating data

### Requirement: Deployment verification coverage
SkyBook SHALL retain automated coverage for production settings and static
configuration and add migration, seed, and booking behavior coverage compatible with
SQLite development and PostgreSQL production. Release verification SHALL cover tests,
formatting, linting, Django checks, migration drift, strict OpenSpec validation, and
diff whitespace checks while retaining existing production checks.

#### Scenario: Contributor verifies the redesigned flow
- **WHEN** the documented verification sequence is run
- **THEN** the connected-flow tests and existing Render production settings tests pass
  without changing database-selection or deployment security behavior

