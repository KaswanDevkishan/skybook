## ADDED Requirements

### Requirement: Runnable generated Django project
After the course phase gate is approved, SkyBook SHALL run as a Django project created
with `django-admin`, and its main `reservations` application SHALL be created with
`manage.py startapp`.

#### Scenario: Development server starts
- **WHEN** a contributor installs the documented dependencies and runs the documented
  Django development command
- **THEN** Django starts with the SkyBook settings without importing Flask

#### Scenario: Main application is installed
- **WHEN** Django loads the project settings
- **THEN** the generated `reservations` application is present in the installed
  applications

### Requirement: SQLite development database
The Django development configuration SHALL use SQLite and SHALL keep local database
files out of version control.

#### Scenario: Clean development database is initialized
- **WHEN** a contributor applies migrations without overriding database configuration
- **THEN** Django creates or updates a local SQLite database

### Requirement: Administrative model access
The Django administrative site SHALL register `City`, `Airline`, `Flight`, `Seat`, and
`Booking`.

#### Scenario: Administrator inspects domain records
- **WHEN** an authenticated staff user opens the Django admin site
- **THEN** each SkyBook domain model is available for administration

### Requirement: Reproducible framework quality workflow
Project configuration and CI SHALL provide documented `uv`, Ruff, Pytest, coverage,
and Django migration-check commands that work with the generated Django structure.

#### Scenario: Contributor runs verification
- **WHEN** a contributor follows the documented verification commands
- **THEN** formatting, linting, model tests, coverage, and migration drift checks run
  against the Django project

### Requirement: Deferred product features
The initial Django project SHALL NOT provide flight-search pages, a seat-map interface,
authentication pages, payment features, or a complete booking workflow.

#### Scenario: Initial application scope is reviewed
- **WHEN** a contributor inspects the routes, templates, and application services
- **THEN** only Django foundation, admin, schema, and test behavior required by this
  change are present

### Requirement: Obsolete Flask runtime removal
After the approved transition, the repository SHALL NOT retain Flask as a runtime
dependency or expose the obsolete Flask application entry point.

#### Scenario: Framework replacement is verified
- **WHEN** a contributor searches runtime dependencies and entry points after the
  transition
- **THEN** the project uses Django without an active Flask scaffold
