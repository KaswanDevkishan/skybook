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
Repository guidance SHALL identify the current work as Exercise 8 and SHALL permit
proper Django forms for GET flight search and POST guest booking creation in addition
to the existing Django foundation, schema, administration, and basic views. It SHALL
continue to prohibit authentication screens, payments, an interactive seat-map
interface, external airline APIs, production styling, and a complete booking
workflow. It SHALL direct contributors not to add seat class or another schema field
unless a later requirement genuinely requires it.

#### Scenario: Exercise 8 form feature is requested
- **WHEN** an agent prepares validated flight search or simple guest booking form work
- **THEN** repository guidance identifies that focused work as permitted within
  Exercise 8

#### Scenario: Deferred feature is requested
- **WHEN** a requested task would add authentication UI, payments, an interactive
  seat map, an external airline integration, or a complete booking workflow
- **THEN** the guidance identifies that work as outside the Exercise 8 scope

### Requirement: Domain constraints remain documented
Guidance SHALL identify `City`, `Airline`, `Flight`, `Seat`, Django's built-in
authentication user, and `Booking` as implemented schema entities. It SHALL document
guest and registered-user bookings and database-backed prevention of duplicate seat
bookings as implemented invariants.

#### Scenario: Agent reviews booking requirements
- **WHEN** an agent reads project documentation
- **THEN** it distinguishes implemented schema guarantees from deferred user-facing
  booking functionality

### Requirement: Repository hygiene
Guidance and Git exclusions SHALL cover tokens, passwords, `.env` files, virtual
environments, caches, coverage artifacts, and local SQLite/database files, while making
clear that ignore patterns do not authorize storing secrets.

#### Scenario: Local development creates generated or sensitive files
- **WHEN** standard local environment, cache, coverage, secret, or database files appear
- **THEN** Git excludes them and contributor guidance says they must not be committed
