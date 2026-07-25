## Why

SkyBook needs an initial runnable application and relational schema for the next course
phase so later search and booking exercises can build on explicit, tested domain
objects. This work is not allowed within the repository's current Exercise 4 scope:
implementation must wait until the course phase advances and the accompanying guidance
change is approved.

## What Changes

- **BREAKING** Replace the minimal Flask scaffold and Flask dependency with a
  `django-admin`-generated Django project and a `manage.py startapp` application.
- Keep SQLite as the development database and retain `uv`, Ruff, Pytest, and coverage
  as the project workflow, adding only the Django integration needed by those tools.
- Add `City`, `Airline`, `Flight`, `Seat`, and `Booking` models, using Django's built-in
  authentication user model and allowing a null booking user for guests.
- Define database constraints that protect core model invariants, including unique
  flight-seat assignments and valid flight timing, and add useful string
  representations.
- Register all domain models in Django admin, create migrations, and verify that the
  initial migration applies to a clean SQLite database.
- Add unit tests for model relationships, constraints, and string representations.
- Update `README.md`, `AGENTS.md`, and OpenSpec documentation to reflect the approved
  framework and course phase.
- Remove obsolete Flask entry points, tests, dependencies, and documentation.
- Preserve flight search, seat-map UI, authentication pages, payment, and the complete
  booking workflow as deferred features.
- Until this change is approved for a post-Exercise-4 phase, preserving Flask and
  deferring all application-feature implementation remain repository requirements.

## Capabilities

### New Capabilities

- `django-project-foundation`: Defines the runnable Django project, main application,
  SQLite development setup, admin integration, and framework-aligned quality workflow.
- `reservation-data-model`: Defines the initial airline reservation entities,
  relationships, guest-booking support, constraints, migrations, and model
  representations.

### Modified Capabilities

- `repository-agent-guidance`: Replaces the Flask-only and Exercise 4 implementation
  prohibition after phase approval with accurate Django structure, commands, scope,
  and deferred-feature guidance.

## Impact

The change affects the application framework, entry point, dependency metadata, test
configuration, CI assumptions, database migrations, admin site, contributor guidance,
and OpenSpec requirements. Existing Flask code is removed rather than maintained in
parallel. GitHub issues #2, #3, and #4 are addressed at the project-foundation,
application, and schema layers; no end-user booking pages or workflow are introduced.
