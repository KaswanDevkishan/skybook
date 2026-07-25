## MODIFIED Requirements

### Requirement: Consistent project identity
After the post-Exercise-4 transition is approved, repository guidance SHALL identify
SkyBook as a Python 3.12, Django, SQLite airline reservation course project and SHALL
NOT direct contributors or agents to restore the obsolete Flask scaffold.

#### Scenario: Agent selects a web framework
- **WHEN** an agent reads the repository guidance after the approved transition
- **THEN** it finds Django identified as the required framework and Flask restoration
  prohibited

### Requirement: Accurate repository and tooling guidance
Contributor documentation SHALL reflect the checked-in Django repository structure and
SHALL document the `uv` setup and Django run commands plus the Ruff formatting, Ruff
linting, Pytest, coverage, and migration-check commands configured by `pyproject.toml`
and CI.

#### Scenario: Contributor verifies the project
- **WHEN** a contributor follows the documented quality commands
- **THEN** formatting, linting, tests, application coverage, and migration drift checks
  run with the repository's configured tools

### Requirement: Exercise 4 scope boundary
Before the course phase transition is explicitly approved, repository guidance SHALL
continue to prohibit application-feature implementation, including the Django
conversion and database models. After approval, guidance SHALL permit only the Django
foundation and schema work specified by this change while continuing to defer flight
search, the seat-map interface, authentication pages, payment, and the complete booking
workflow.

#### Scenario: Change is applied before phase approval
- **WHEN** an agent is asked to implement this change while Exercise 4 remains active
- **THEN** the guidance identifies the implementation as outside the current scope

#### Scenario: Change is applied after phase approval
- **WHEN** an agent implements the approved initial Django and schema milestone
- **THEN** the guidance permits foundation, model, admin, migration, test, and
  documentation work while preserving the deferred-feature boundary

### Requirement: Domain constraints remain documented
Guidance SHALL identify `City`, `Airline`, `Flight`, `Seat`, Django's built-in
authentication user, and `Booking` as implemented schema entities after this change.
It SHALL describe guest and registered-user bookings and database-backed prevention of
duplicate seat bookings as implemented invariants while distinguishing flight search,
seat maps, authentication pages, payment, and complete booking behavior as planned
future work.

#### Scenario: Agent reviews booking requirements
- **WHEN** an agent reads project documentation after this change
- **THEN** it can distinguish implemented schema guarantees from deferred user-facing
  booking functionality
