## ADDED Requirements

### Requirement: Consistent project identity
Repository guidance SHALL identify SkyBook as a Python 3.12, Flask 3, SQLite airline
reservation course project and SHALL NOT direct contributors or agents to convert it
to Django.

#### Scenario: Agent selects a web framework
- **WHEN** an agent reads the repository guidance before planning work
- **THEN** it finds Flask identified as the required framework and Django conversion
  prohibited

### Requirement: Accurate repository and tooling guidance
Contributor documentation SHALL reflect the checked-in repository structure and SHALL
document the `uv` setup and run commands plus the Ruff formatting, Ruff linting, Pytest,
and coverage commands configured by `pyproject.toml` and CI.

#### Scenario: Contributor verifies the project
- **WHEN** a contributor follows the documented quality commands
- **THEN** formatting, linting, tests, and application coverage run with the repository's
  configured tools

### Requirement: OpenSpec-first implementation workflow
Agent guidance and OpenSpec configuration SHALL require relevant OpenSpec documents to
be read before meaningful implementation and SHALL describe the project constraints
needed to plan changes safely.

#### Scenario: Agent begins meaningful implementation
- **WHEN** an agent prepares to modify project behavior or structure
- **THEN** it first reviews the relevant OpenSpec artifacts and applies their constraints

### Requirement: Exercise 4 scope boundary
Repository guidance SHALL prohibit application-feature implementation during Exercise
4, including database models, flight search, booking, authentication, and the seat-map
interface.

#### Scenario: Feature work is proposed during Exercise 4
- **WHEN** a requested task would implement a deferred application feature
- **THEN** the guidance identifies that work as outside the current exercise scope

### Requirement: Domain constraints remain documented
Guidance SHALL retain the planned `City`, `Airline`, `Flight`, `Seat`, `User`, and
`Booking` entities, guest and registered bookings, and server-side prevention of
duplicate seat bookings as future implementation constraints rather than current
features.

#### Scenario: Agent reviews future booking requirements
- **WHEN** an agent reads the project documentation
- **THEN** it can distinguish planned domain behavior from functionality already present

### Requirement: Repository hygiene
Guidance and Git exclusions SHALL cover tokens, passwords, `.env` files, virtual
environments, caches, coverage artifacts, and local SQLite/database files, while making
clear that ignore patterns do not authorize storing secrets.

#### Scenario: Local development creates generated or sensitive files
- **WHEN** standard local environment, cache, coverage, secret, or database files appear
- **THEN** Git excludes them and contributor guidance says they must not be committed
